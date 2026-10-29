import unittest
from main import ClinicSystem, Patient, Doctor, TimeSlot


class TestClinicSystem(unittest.TestCase):
    def setUp(self):
        self.system = ClinicSystem(max_appointments=3)
        self.doctor = Doctor("D1", "Dr. Adams")
        self.patient = Patient("P1", "Alice")
        self.slot1 = TimeSlot("S1", "2026-11-01 10:00")
        self.slot2 = TimeSlot("S2", "2026-11-01 11:00")
        self.slot3 = TimeSlot("S3", "2026-11-01 12:00")
        self.slot4 = TimeSlot("S4", "2026-11-01 13:00")

        self.doctor.add_slot(self.slot1)
        self.doctor.add_slot(self.slot2)
        self.doctor.add_slot(self.slot3)
        self.doctor.add_slot(self.slot4)

        self.system.register_doctor(self.doctor)
        self.system.register_patient(self.patient)

    def test_book_and_limit_enforcement(self):
        self.system.book_appointment("P1", "D1", "S1")
        self.system.book_appointment("P1", "D1", "S2")
        self.system.book_appointment("P1", "D1", "S3")

        self.assertEqual(self.patient.get_upcoming_count(), 3)
        with self.assertRaises(ValueError):
            self.system.book_appointment("P1", "D1", "S4")

    def test_doctor_decline_frees_slot(self):
        appt = self.system.book_appointment("P1", "D1", "S1")
        self.assertFalse(self.slot1.is_available)
        self.system.respond_to_appointment(appt.appointment_id, accept=False)
        self.assertEqual(appt.status, "DECLINED")
        self.assertTrue(self.slot1.is_available)


if _name_ == "_main_":
    unittest.main()
