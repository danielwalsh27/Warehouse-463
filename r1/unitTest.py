import unittest
import main

class TestStringMethods(unittest.TestCase):
    def test_1_initial_warehouses(self):
        print("Testing Null Warehouse List")
        self.assertEqual(main.warehouses, [])
        print("Test 1 PASS")
        
    def test_2_add_warehouse(self):
        print("Testing Add Warehouse")
        main.warehouseWidth.text = 5
        main.warehouseHeight.text = 5
        main.onWarehouseDimensionButtonClicked()
        self.assertEqual(len(main.warehouses), 1)
        self.assertEqual(main.warehouses[0].width, 5)
        main.warehouses = []
        main.warehouseHeight.text = ""
        main.warehouseWidth.text = ""
        print("Test 2 PASS")
        
    def test_3_testMaxArea_spaceUsed_spaceRemaining(self):
        print("Testing Max Area, Space Used & Space Remaining")
        main.warehouseWidth.text = 15
        main.warehouseHeight.text = 15
        main.onWarehouseDimensionButtonClicked()
        main.warehouses[0].getRemainingSpace()
        main.warehouses[0].usedSpace()
        self.assertEqual(main.warehouses[0].area, 225)
        self.assertEqual(main.warehouses[0].usedArea, 0)
        main.warehouses = []
        main.warehouseHeight.text = ""
        main.warehouseWidth.text = ""
        print("Test 3 PASS")

<<<<<<< HEAD
    def test4_addbox(self):
        print("\nTesting adding boxes, correct positioning")
        dummyhouse = main.warehouse(10, 10, 720, 720)
        main.warehouses.append(dummyhouse)
        main.createObjectName.text = 'box1'
        main.createObjectWidth.text = '2'
        main.createObjectHeight.text = '2'
        main.onAddBoxButtonClicked()

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
=======
    def test_box_delete_if_exist(self):
        print("Testing deleting existing box")
        self.assertEqual(len(main.warehouses), 0)
        main.warehouses = []
        main.onPrintListClicked()
        print("Test 4.5 PASS")
>>>>>>> master

if __name__ == '__main__':
    main.pg.display.iconify()
    unittest.main()
