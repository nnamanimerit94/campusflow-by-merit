# CampusFlow Baseline Check

## 1. Purpose

This document records the condition of the original CampusFlow
application before implementing CampusFlow Next improvements.

The objective is to establish a verified baseline, identify
existing issues, and protect original functionality against
regressions during Assessment 2.

## 2. Application Verification

Command:

python3 main.py

Result: PASS

The application started successfully and displayed the
interactive CampusFlow menu.

## 3. Automated Tests

Command:

python3 -m unittest discover -s tests -v

Results:

- Tests executed: 119
- Tests passed: 119
- Failures: 0
- Errors: 0
- Execution time: 0.182 seconds

Status: PASS

## 4. Manual Testing

### Test 1: Ticket Creation and Priority

Created ticket T001:

- Title: wifi is down
- Category: Network
- Urgency: low
- Affected users: 40
- Calculated priority: high

Created ticket T002:

- Title: pebbles
- Category: Other
- Urgency: low
- Affected users: 4
- Calculated priority: medium

Both tickets were created successfully.

Status: PASS

### Test 2: Ticket Assignment and Lifecycle

Assigned ticket T001 to kingsley.

Verified the following transitions:

open -> in_progress -> resolved -> open

Attempted to reopen T001 while in_progress.

The application correctly rejected the operation.

After resolving T001, reopening succeeded.

The assignment to kingsley remained unchanged.

Status: PASS

### Test 3: JSON Persistence

Exited and restarted CampusFlow.

Retrieved ticket T001 using the ticket details menu.

The application preserved:

- Ticket ID: T001
- Status: in_progress
- Assigned mentor: kingsley

Status: PASS

### Test 4: Work Queue and Reports

The Open Work Queue excluded ticket T001 while it
was in_progress.

The reports correctly showed:

- Total tickets: 2
- Open: 1
- In progress: 1
- Resolved: 0
- High priority: 1
- Medium priority: 1

Status: PASS

## 5. Confirmed Baseline Issue

### Missing Data Directory

During initial manual testing, ticket creation failed
because the application attempted to save a temporary
JSON file inside a missing root-level data directory.

Observed error:

No such file or directory: .../campusflow-by-merit/data/tmp...

Temporary workaround:

mkdir -p data

After creating the directory, ticket saving succeeded.

This issue should be considered during the CampusFlow
Next persistence reliability improvements.

## 6. Assessment 2 Improvement Areas

The CampusFlow Next assessment requires improvements to:

1. Ticket validation and lifecycle safety.
2. Structured ticket follow-up notes.
3. Multi-filter ticket search.
4. Reporting and analytics.
5. JSON validation, safe reload, and ID continuity.
6. Automated tests and edge-case coverage.
7. CLI engineering understanding checks.
8. Documentation and peer review evidence.

These are assessment requirements, not necessarily
confirmed defects in the original application.

## 7. Baseline Conclusion

The original CampusFlow application passed all 119
automated tests.

Manual testing confirmed ticket creation, priority
calculation, assignment, status transitions, reopening,
work queue behavior, reporting, and persistence across
an application restart.

One environment/setup issue was confirmed: the application
could not save tickets when the root-level data directory
was missing.

The baseline is established and can be used to evaluate
CampusFlow Next improvements.