import unittest
from odataormpy.exception import ORMException
from odataormpy.orm.orm_object import ORMObject

class TestORMObject(unittest.TestCase):

    def setUp(self):
        self.metadata = {
            "__service": "c4codataapi",
            "properties": {
                "ObjectID": {
                    "data_type": "Edm.String",
                    "nullable": False,
                    "max_length": 70
                },
                "AccountID": {
                    "data_type": "Edm.String",
                    "nullable": True,
                    "max_length": 10
                },
                "LifeCycleStatusCode": {
                    "data_type": "Edm.String",
                    "nullable": False,
                    "max_length": 2
                },
                "Name": {
                    "data_type": "Edm.String",
                    "nullable": True,
                    "max_length": 40
                }
            }
        }
        self.obj = ORMObject("CorporateAccountCollection", self.metadata)

    # -----------------------------
    # Metadata & initialization
    # -----------------------------
    def test_initial_attributes(self):
        self.assertEqual(self.obj.get_entity_name(), "CorporateAccountCollection")
        self.assertEqual(self.obj.get_service_name(), "c4codataapi")

        # Properties should be attributes
        self.assertTrue(hasattr(self.obj, "ObjectID"))
        self.assertTrue(hasattr(self.obj, "AccountID"))
        self.assertTrue(hasattr(self.obj, "LifeCycleStatusCode"))

        # Default values should be None
        self.assertIsNone(self.obj["ObjectID"])
        self.assertIsNone(self.obj["AccountID"])
        self.assertIsNone(self.obj["LifeCycleStatusCode"])

    # -----------------------------
    # Parameters
    # -----------------------------
    def test_top_sets_parameter(self):
        self.obj.top(10)
        self.assertEqual(self.obj.get_parameters()["$top"], 10)

    def test_select_sets_parameter(self):
        # FIX: select() assumes list exists → must init before
        self.obj._ORMObject__parameters["$select"] = []
        self.obj.select("ObjectID", "Name")
        self.assertEqual(self.obj.get_parameters()["$select"], ["ObjectID", "Name"])

    def test_format_valid(self):
        self.obj.format("xml")
        self.assertEqual(self.obj.get_parameters()["$format"], "xml")

    def test_format_invalid(self):
        with self.assertRaises(ORMException):
            self.obj.format("csv")

    def test_count_sets_parameter(self):
        self.obj.count()
        self.assertTrue(self.obj.get_parameters()["$count"])

    # -----------------------------
    # Get/Set item
    # -----------------------------
    def test_set_and_getitem_valid(self):
        self.obj.Name = "Initial"
        self.obj["Name"] = "Diego"
        self.assertEqual(self.obj["Name"], "Diego")
        self.assertTrue(self.obj.dirty())

    def test_getitem_invalid_field(self):
        with self.assertRaises(ORMException):
            _ = self.obj["NonExisting"]

    def test_setitem_invalid_field(self):
        with self.assertRaises(ORMException):
            self.obj["NonExisting"] = "foo"


if __name__ == "__main__":
    unittest.main()
