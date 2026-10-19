import json
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

import main


class TestCampusFlowCLI(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        self.test_file = (
            Path(self.temp_directory.name) / "tickets.json"
        )

        self.file_patch = patch.object(
            main,
            "FILE_PATH",
            str(self.test_file)
        )

        self.file_patch.start()

    def tearDown(self):
        self.file_patch.stop()
        self.temp_directory.cleanup()

    def run_cli(self, inputs):
        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print"):
                main.main()

    def read_tickets(self):
        with open(self.test_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def sample_ticket(self, status="open", assigned_to=None):
        return {
            "id": "T001",
            "title": "Wi-Fi is down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 5,
            "priority": "high",
            "status": status,
            "assigned_to": assigned_to,
        }

    def save_sample_ticket(self, status="open", assigned_to=None):
        ticket = self.sample_ticket(status, assigned_to)

        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump({"T001": ticket}, file)

    # TEST 1: EXIT APPLICATION
    def test_exit_application(self):
        self.run_cli(["0"])

        self.assertFalse(self.test_file.exists())

    # TEST 2: CREATE TICKET
    def test_create_ticket(self):
        self.run_cli([
            "1",
            "Wi-Fi is down",
            "Network",
            "high",
            "5",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertIn("T001", tickets)
        self.assertEqual(
            tickets["T001"]["title"],
            "Wi-Fi is down"
        )
        self.assertEqual(
            tickets["T001"]["status"],
            "open"
        )

    # TEST 3: INVALID TITLE
    def test_invalid_title_then_valid_title(self):
        self.run_cli([
            "1",
            "",
            "Wi-Fi is down",
            "Network",
            "high",
            "5",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(len(tickets), 1)
        self.assertEqual(
            tickets["T001"]["title"],
            "Wi-Fi is down"
        )

    # TEST 4: INVALID CATEGORY
    def test_invalid_category_then_valid_category(self):
        self.run_cli([
            "1",
            "Wi-Fi is down",
            "Invalid",
            "Network",
            "high",
            "5",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["category"],
            "Network"
        )

    # TEST 5: INVALID URGENCY
    def test_invalid_urgency_then_valid_urgency(self):
        self.run_cli([
            "1",
            "Wi-Fi is down",
            "Network",
            "urgent",
            "high",
            "5",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["urgency"],
            "high"
        )

    # TEST 6: INVALID AFFECTED USERS
    def test_invalid_affected_users_then_valid_number(self):
        self.run_cli([
            "1",
            "Wi-Fi is down",
            "Network",
            "high",
            "abc",
            "0",
            "5",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["affected_users"],
            5
        )

    # TEST 7: LOAD EXISTING TICKETS
    def test_load_existing_tickets(self):
        self.save_sample_ticket()

        self.run_cli(["0"])

        tickets = self.read_tickets()

        self.assertIn("T001", tickets)

    # TEST 8: CREATE TICKET WITHOUT LOSING EXISTING DATA
    def test_create_ticket_preserves_existing_tickets(self):
        self.save_sample_ticket()

        self.run_cli([
            "1",
            "Computer not working",
            "Hardware",
            "medium",
            "2",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertIn("T001", tickets)
        self.assertIn("T002", tickets)
        self.assertEqual(len(tickets), 2)

    # TEST 9: ASSIGN TICKET
    def test_assign_ticket(self):
        self.save_sample_ticket()

        self.run_cli([
            "3",
            "T001",
            "Kingsley",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["assigned_to"],
            "Kingsley"
        )

    # TEST 10: UPDATE STATUS TO IN PROGRESS
    def test_start_working_on_ticket(self):
        self.save_sample_ticket(assigned_to="Kingsley")

        self.run_cli([
            "5",
            "T001",
            "in_progress",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["status"],
            "in_progress"
        )

    # TEST 11: RESOLVE TICKET
    def test_resolve_ticket(self):
        self.save_sample_ticket(
            status="in_progress",
            assigned_to="Kingsley"
        )

        self.run_cli([
            "5",
            "T001",
            "resolved",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["status"],
            "resolved"
        )

    # TEST 12: REOPEN TICKET
    def test_reopen_ticket(self):
        self.save_sample_ticket(
            status="resolved",
            assigned_to="Kingsley"
        )

        self.run_cli([
            "6",
            "T001",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["status"],
            "open"
        )

    # TEST 13: REJECT INVALID STATUS TRANSITION
    def test_cannot_resolve_open_ticket_directly(self):
        self.save_sample_ticket(assigned_to="Kingsley")

        self.run_cli([
            "5",
            "T001",
            "resolved",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["status"],
            "open"
        )

    # TEST 14: REJECT UNASSIGNED WORK
    def test_cannot_start_unassigned_ticket(self):
        self.save_sample_ticket()

        self.run_cli([
            "5",
            "T001",
            "in_progress",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["status"],
            "open"
        )

    # TEST 15: INVALID MENU CHOICE
    def test_invalid_menu_choice(self):
        self.run_cli([
            "99",
            "0",
        ])

        self.assertFalse(self.test_file.exists())

    # TEST 16: VIEW ALL TICKETS
    def test_view_all_tickets(self):
        self.save_sample_ticket()

        self.run_cli([
            "2",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertIn("T001", tickets)

    # TEST 17: VIEW TICKET DETAILS
    def test_view_ticket_details(self):
        self.save_sample_ticket()

        self.run_cli([
            "4",
            "T001",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertIn("T001", tickets)

    # TEST 18: VIEW OPEN WORK QUEUE
    def test_view_open_work_queue(self):
        self.save_sample_ticket()

        self.run_cli([
            "7",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["status"],
            "open"
        )

    # TEST 19: VIEW REPORTS
    def test_view_reports(self):
        self.save_sample_ticket()

        self.run_cli([
            "8",
            "0",
        ])

        tickets = self.read_tickets()

        self.assertEqual(len(tickets), 1)

    # TEST 20: CORRUPTED JSON
    def test_corrupted_json_stops_application(self):
        self.test_file.write_text(
            "{invalid json",
            encoding="utf-8"
        )

        self.run_cli(["0"])

        self.assertEqual(
            self.test_file.read_text(encoding="utf-8"),
            "{invalid json"
        )

    # TEST 21: SAVE FAILURE
    def test_save_failure_does_not_create_ticket(self):
        with patch.object(
            main,
            "save_tickets",
            side_effect=OSError("Disk error")
        ):
            self.run_cli([
                "1",
                "Wi-Fi is down",
                "Network",
                "high",
                "5",
                "0",
            ])

        self.assertFalse(self.test_file.exists())

    # TEST 22: SAVE FAILURE ROLLS BACK ASSIGNMENT
    def test_assignment_save_failure(self):
        self.save_sample_ticket()

        with patch.object(
            main,
            "save_tickets",
            side_effect=OSError("Disk error")
        ):
            self.run_cli([
                "3",
                "T001",
                "Kingsley",
                "0",
            ])

        tickets = self.read_tickets()

        self.assertIsNone(
            tickets["T001"]["assigned_to"]
        )

    # TEST 23: SAVE FAILURE ROLLS BACK STATUS
    def test_status_save_failure(self):
        self.save_sample_ticket(assigned_to="Kingsley")

        with patch.object(
            main,
            "save_tickets",
            side_effect=OSError("Disk error")
        ):
            self.run_cli([
                "5",
                "T001",
                "in_progress",
                "0",
            ])

        tickets = self.read_tickets()

        self.assertEqual(
            tickets["T001"]["status"],
            "open"
        )


if __name__ == "__main__":
    unittest.main()