"""
Clinic Appointment Booking System
Matches requirements R1-R7 and designed Class/Sequence diagrams.
"""

MAX_UPCOMING_APPOINTMENTS = 3  # N parameter (R4)


class TimeSlot:
    def _init_(self, slot_id: str, date_time: str):
        self.slot_id = slot_id
        self.date_time = date_time
        self.is_available = True

    def _repr_(self):
        return f"<Slot {self.slot_id}: {self.date_time} (Available: {self.is_available})>"


class Patient:
    def _init_(self, patient_id: str, name: str):
        self.patient_id = patient_id
        self.name = name
        self.appointments = []

    def get_upcoming_count(self) -> int:
        return sum(1 for appt in self.appointments if appt.status in ["PENDING", "CONFIRMED"])


class Doctor:
    def _init_(self, doctor_id: str, name: str):
        self.doctor_id = doctor_id
        self.name = name
        self.availability = []

    def add_slot(self, slot: TimeSlot):
        self.availability.append(slot)


class Appointment:
    def _init_(self, appointment_id: str, patient: Patient, doctor: Doctor, time_slot: TimeSlot):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.time_slot = time_slot
        self.status = "PENDING"

    def confirm(self):
        self.status = "CONFIRMED"

    def decline(self):
        self.status = "DECLINED"
        self.time_slot.is_available = True


class ClinicSystem:
    def _init_(self, max_appointments: int = MAX_UPCOMING_APPOINTMENTS):
        self.max_appointments = max_appointments
        self.doctors = {}
        self.patients = {}
        self.appointments = {}

    def register_patient(self, patient: Patient):
        self.patients[patient.patient_id] = patient

    def register_doctor(self, doctor: Doctor):
        self.doctors[doctor.doctor_id] = doctor

    def get_available_slots(self, doctor_id: str):
        """R1: Patient views available days and times."""
        doctor = self.doctors.get(doctor_id)
        if not doctor:
            return []
        return [slot for slot in doctor.availability if slot.is_available]

    def book_appointment(self, patient_id: str, doctor_id: str, slot_id: str) -> Appointment:
        """R2 & R4: Book appointment with max limit enforcement."""
        patient = self.patients.get(patient_id)
        doctor = self.doctors.get(doctor_id)

        if not patient or not doctor:
            raise ValueError("Patient or Doctor not found.")

        # Enforcement of R4: N upcoming appointments limit
        if patient.get_upcoming_count() >= self.max_appointments:
            raise ValueError(f"Booking failed: Patient reached maximum limit of {self.max_appointments} upcoming appointments.")

        slot = next((s for s in doctor.availability if s.slot_id == slot_id and s.is_available), None)
        if not slot:
            raise ValueError("Selected time slot is not available.")

        slot.is_available = False
        appt_id = f"APP-{len(self.appointments) + 1}"
        appointment = Appointment(appt_id, patient, doctor, slot)

        patient.appointments.append(appointment)
        self.appointments[appt_id] = appointment
        return appointment

    def respond_to_appointment(self, appointment_id: str, accept: bool) -> bool:
        """R3: Doctor accepts or declines an appointment request."""
        appointment = self.appointments.get(appointment_id)
        if not appointment or appointment.status != "PENDING":
            return False

        if accept:
            appointment.confirm()
        else:
            appointment.decline()
        return True


if _name_ == "_main_":
    print("=== Initializing Clinic System ===")
    system = ClinicSystem(max_appointments=3)

    # Setup Demo Data
    doc = Doctor("D101", "Dr. Sarah Smith")
    slot1 = TimeSlot("S1", "2026-11-01 09:00 AM")
    slot2 = TimeSlot("S2", "2026-11-01 10:00 AM")
    slot3 = TimeSlot("S3", "2026-11-01 11:00 AM")
    slot4 = TimeSlot("S4", "2026-11-01 02:00 PM")
    doc.add_slot(slot1)
    doc.add_slot(slot2)
    doc.add_slot(slot3)
    doc.add_slot(slot4)

    pat = Patient("P201", "John Doe")
    system.register_doctor(doc)
    system.register_patient(pat)

    print("\n--- R1: View Available Slots ---")
    available = system.get_available_slots("D101")
    for s in available:
        print(s)

    print("\n--- R2: Booking Appointments ---")
    a1 = system.book_appointment("P201", "D101", "S1")
    print(f"Booked: {a1.appointment_id} - Status: {a1.status}")

    a2 = system.book_appointment("P201", "D101", "S2")
    print(f"Booked: {a2.appointment_id} - Status: {a2.status}")

    a3 = system.book_appointment("P201", "D101", "S3")
    print(f"Booked: {a3.appointment_id} - Status: {a3.status}")

    print("\n--- R4: Testing Appointment Limit (N=3) ---")
    try:
        a4 = system.book_appointment("P201", "D101", "S4")
    except ValueError as e:
        print(f"Expected Error caught: {e}")

    print("\n--- R3: Doctor Accepting & Declining ---")
    print(f"Appointment {a1.appointment_id} status before: {a1.status}")
    system.respond_to_appointment(a1.appointment_id, accept=True)
    print(f"Appointment {a1.appointment_id} status after Accept: {a1.status}")

    print(f"Appointment {a2.appointment_id} status before: {a2.status}")
    system.respond_to_appointment(a2.appointment_id, accept=False)
    print(f"Appointment {a2.appointment_id} status after Decline: {a2.status}")

    print(f"Upcoming appointments count for {pat.name}: {pat.get_upcoming_count()}")
    print("\n=== All Scenarios Executed Successfully ===")
