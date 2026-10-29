# Use Cases & Diagram (P2 & P3)

## Actors
- **Patient**
- **Doctor**

---

## Use Case 1: View Doctor Availability
- **Primary Actor:** Patient
- **Preconditions:** Patient is logged into the system.
- **Main Success Flow:**
  1. Patient requests available time slots for a specific doctor.
  2. System retrieves and displays open time slots within 2 seconds (R6).
- **Alternative Flow:**
  - **2a. No slots available:** System displays a message stating no available times and prompts the patient to select a different date or doctor.

---

## Use Case 2: Book Appointment
- **Primary Actor:** Patient
- **Preconditions:** Patient views available slots.
- **Main Success Flow:**
  1. Patient selects an available time slot.
  2. System checks if the patient currently has fewer than N (N=3) upcoming appointments (R4).
  3. System creates a pending appointment request.
  4. System notifies the doctor of the pending request.
- **Alternative Flow:**
  - **2a. Appointment limit reached:** If the patient already has 3 upcoming appointments, the system denies the booking request and displays: `"Booking failed: Maximum upcoming appointment limit (3) reached."`

---

## Use Case 3: Review Appointment Request
- **Primary Actor:** Doctor
- **Preconditions:** Doctor has pending appointment requests.
- **Main Success Flow:**
  1. Doctor reviews pending request details.
  2. Doctor accepts the appointment request.
  3. System updates status to `CONFIRMED` and marks the time slot as booked.
- **Alternative Flow:**
  - **2a. Doctor declines request:** Doctor selects decline. System updates status to `DECLINED` and frees up the time slot.

---

## Use Case Diagram (Mermaid)

```mermaid
graph LR
    Patient((Patient))
    Doctor((Doctor))

    subgraph Clinic Appointment System
        UC1[UC1: View Availability]
        UC2[UC2: Book Appointment]
        UC3[UC3: Accept/Decline Request]
    end

    Patient --> UC1
    Patient --> UC2
    Doctor --> UC3