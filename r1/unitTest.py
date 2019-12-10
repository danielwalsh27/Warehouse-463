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

if __name__ == '__main__':
    main.pg.display.iconify()
    unittest.main()
