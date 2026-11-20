from collections import defaultdict
from pathlib import Path


def is_valid_email(email):
  if email.count("@") != 1:
    return False
  local, domain = email.split("@")
  if not local or not domain:
    return False
  if "." not in domain:
    return False
  if email.startswith(".") or email.endswith("."):
    return False
  if ".." in email:
    return False
  return True


def read_department_files(directory_path):
  dir_path = Path(directory_path)
  registrations = []
  error_logs = []
  seen_reg_nos = set()

  for file_path in sorted(dir_path.glob("*.txt")):
    try:
      with open(file_path, mode="r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
          line = raw_line.strip()
          if not line:
            continue
          parts = [p.strip() for p in line.split(",")]
          if len(parts) != 5:
            error_logs.append(
                f"{file_path.name}, Line {line_num}: Invalid field count"
            )
            continue
          reg_no, name, dept, email, events_str = parts

          if not is_valid_email(email):
            error_logs.append(
                f"{file_path.name}, Line {line_num}: Invalid email '{email}'"
            )
            continue

          events = [e.strip() for e in events_str.split(";") if e.strip()]
          if not events:
            error_logs.append(
                f"{file_path.name}, Line {line_num}: No events selected"
            )
            continue

          if reg_no in seen_reg_nos:
            error_logs.append(
                f"{file_path.name}, Line {line_num}: Duplicate registration"
                f" for '{reg_no}'"
            )
            continue

          seen_reg_nos.add(reg_no)
          registrations.append({
              "reg_no": reg_no,
              "name": name,
              "dept": dept,
              "email": email,
              "events": events,
          })
    except Exception as e:
      error_logs.append(f"{file_path.name}, Error: {str(e)}")

  return registrations, error_logs


def process_fest_registrations(directory_path):
  registrations, error_logs = read_department_files(directory_path)

  event_participants = defaultdict(list)
  for reg in registrations:
    for event in reg["events"]:
      event_participants[event].append(reg)

  with open("master_list.txt", mode="w", encoding="utf-8") as f:
    f.write("Register Number,Name,Department,Email,Events\n")
    for reg in registrations:
      events_joined = ";".join(reg["events"])
      f.write(
          f"{reg['reg_no']},{reg['name']},{reg['dept']},{reg['email']},"
          f"{events_joined}\n"
      )

  for event, participants in event_participants.items():
    safe_event_name = "".join(
        c if c.isalnum() else "_" for c in event
    ).lower()
    with open(f"event_{safe_event_name}.txt", mode="w", encoding="utf-8") as f:
      f.write(f"Participants for {event}\n")
      f.write("Register Number,Name,Department,Email\n")
      for p in participants:
        f.write(f"{p['reg_no']},{p['name']},{p['dept']},{p['email']}\n")

  with open("summary_report.txt", mode="w", encoding="utf-8") as f:
    f.write("Fest Registration Summary Report\n")
    f.write(f"Total Valid Registrations: {len(registrations)}\n")
    f.write(f"Total Errors Encountered: {len(error_logs)}\n")
    f.write("Event-wise Participant Counts:\n")
    for event, participants in event_participants.items():
      f.write(f"- {event}: {len(participants)}\n")

  with open("error_log.txt", mode="w", encoding="utf-8") as f:
    f.write("Error Log\n")
    for log in error_logs:
      f.write(log + "\n")


if __name__ == "__main__":
  process_fest_registrations("./fest_records")
```[cite: 11, 12]
