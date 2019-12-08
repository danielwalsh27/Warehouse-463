import unittest
from unittest.mock import patch
import main


class TestWarehouseBoxes(unittest.TestCase):

    def test4_addbox(self):
        dummyhouse = main.warehouse(10, 10, 720, 720)
        main.warehouses.append(dummyhouse)
        main.createObjectName.text = 'box1'
        main.createObjectWidth.text = '2'
        main.createObjectHeight.text = '2'
        main.onAddBoxButtonClicked()
        # self.assertEqual(main.warehouse.getboxlist(dummyhouse), [newbox])

        # Users shall be able to input objects with a name, length and width dimensions, this object shall be placed in
        # the upper left available position
        self.assertEqual(main.warehouse.getboxlist(dummyhouse)[0].name, main.createObjectName.text)
        self.assertEqual(main.warehouse.getboxlist(dummyhouse)[0].x, 0)
        self.assertEqual(main.warehouse.getboxlist(dummyhouse)[0].y, 0)
        self.assertEqual(main.warehouse.getboxlist(dummyhouse)[0].width, int(main.createObjectWidth.text))
        self.assertEqual(main.warehouse.getboxlist(dummyhouse)[0].height, int(main.createObjectHeight.text))
        main.warehouses = []
        main.warehouseHeight.text = ""
        main.warehouseWidth.text = ""
        print("Test 4 PASS")

    def test_7_delete_box(self):
        print("Testing delete object")
        main.warehouseWidth.text = '5'
        main.warehouseHeight.text = '5'
        main.onWarehouseDimensionButtonClicked()
        main.createObjectName.text = "box1"
        main.createObjectWidth.text = '5'
        main.createObjectHeight.text = '3'
        main.onAddBoxButtonClicked()
        main.removeObjectName.text = "invalidname"
        main.onRemoveBoxClicked()
        self.assertEqual(len(main.warehouse.getboxlist(main.warehouses[0])), 1)
        main.removeObjectName.text = "box1"
        main.onRemoveBoxClicked()
        self.assertEqual(len(main.warehouse.getboxlist(main.warehouses[0])), 0)
        main.warehouses = []
        main.warehouseHeight.text = ""
        main.warehouseWidth.text = ""
        print("Test 7 PASS")


if __name__ == '__main__':
    main.pg.display.iconify()
    unittest.main()