#  Copyright (C) 2014  Statoil ASA, Norway. 
#   
#  The file 'fault_block_collection.py' is part of ERT - Ensemble based Reservoir Tool. 
#   
#  ERT is free software: you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation, either version 3 of the License, or 
#  (at your option) any later version. 
#   
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY 
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#  FITNESS FOR A PARTICULAR PURPOSE.   
#   
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html> 
#  for more details. 


from ert.cwrap import BaseCClass, CWrapper
from ert.ecl import ECL_LIB


class FaultBlockCollection(BaseCClass):

    def __init__(self , grid , fault_block_kw):
        c_pointer = self.cNamespace().alloc( grid , fault_block_kw)
        if c_pointer:
            super(FaultBlockCollection, self).__init__(c_pointer)
        else:
            raise ValueError("Invalid input - failed to create FaultBlockCollection")

# The underlying C implementation uses lazy evaluation and needs to hold on
# to the grid and kw references. We therefor take references to them here, to protect
# against premature garbage collection.
        self.grid_ref = grid
        self.kw_ref = fault_block_kw


    def __len__(self):
        return self.cNamespace().num_layers(self)
        

    def __getitem__(self , index):
        if isinstance(index, int):
            if index >= 0 and index < len(self):
                return self.cNamespace().get_layer( self , index )
            else:
                raise IndexError
        else:
            raise TypeError("Index should be integer type")


    def getLayer(self , k):
        return self[k]

    def free(self):
        self.cNamespace().free(self)

    def size(self):
        return len(self)

    

cwrapper = CWrapper(ECL_LIB)
CWrapper.registerObjectType("fault_block_collection", FaultBlockCollection)


FaultBlockCollection.cNamespace().alloc      = cwrapper.prototype("c_void_p         fault_block_collection_alloc(ecl_grid , ecl_kw )")
FaultBlockCollection.cNamespace().free       = cwrapper.prototype("void             fault_block_collection_free(fault_block_collection)")
FaultBlockCollection.cNamespace().num_layers = cwrapper.prototype("int              fault_block_collection_num_layers(fault_block_collection)")
FaultBlockCollection.cNamespace().get_layer  = cwrapper.prototype("fault_block_layer_ref  fault_block_collection_get_layer(fault_block_collection, int)")
