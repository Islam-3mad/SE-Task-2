#### 5. 3_candidate_classes.md

`markdown
# Candidate Classes Analysis (P4)

| Candidate Class | Source / Evidence | Category | Justification |
|---|---|---|---|
| Patient | Mentioned in R1, R2, R4 | Explicit | Primary user domain entity. Represents patient state and appointment counts. |
| Doctor | Mentioned in R1, R3 | Explicit | User domain entity who manages time slots and accepts/declines requests. |
| Appointment | Mentioned in R2, R3, R4 | Explicit | Core business entity tracking slot, status, patient, and doctor. |
| TimeSlot | Mentioned in R2 | Explicit | Domain concept representing date, time, and availability state. |
| AppointmentStatus | Inferred from R3 (accept/decline) | Inferred | Enum/State representing statuses: PENDING, CONFIRMED, DECLINED, CANCELLED. |
| ClinicSystem | Inferred system coordinator | Inferred | Controller/Service class orchestrating business logic and validation rules (N limit). |
| Database/Storage | Implied persistence | Rejected | Low-level technical implementation detail; omitted from domain class design. |
| MobileScreen | Mentioned in R7 | Rejected | UI layout requirement, not a core domain model entity. |
