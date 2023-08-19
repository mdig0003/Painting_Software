from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer, get_layers
from data_structures.array_sorted_list import ArraySortedList
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

class LayerStore(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        pass
    """
    Add a layer to the store.
    Returns true if the LayerStore was actually changed.
    """

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        pass

        # initialise the coordinate where the square is coloured using x and y
        # what is the purpose of timestamp
    
    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        pass

        
        # use timestamp to determine when the layer was set
        # erase 
        #
        
    @abstractmethod
    def special(self):
        pass
      
class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self) -> None:
        super().__init__()
        self.layer = None
        self.getcolour = None
        self.get_colour_spec = None
        self.special_func = False
        
    def add(self, layer:Layer):
        if layer is not None:
            self.layer = layer
            return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        self.getcolour =  start
        if self.layer is not None:
            self.getcolour = self.layer.apply(start,timestamp,x,y)

        if self.special_func:
            self.getcolour = (255 - self.getcolour[0], 255 - self.getcolour[1] , 255 - self.getcolour[2])

        return self.getcolour
        
    
    def erase(self, layer: Layer) -> bool:
        if self.layer == None: 
            return False
        self.layer = None
        return True    

    def special(self):
            self.special_func = not self.special_func
    
class AdditiveLayerStore(LayerStore):

    def __init__(self) -> None:
        self.layer = None # sets layer to none hence it starts at default colour 
        self.queue = CircularQueue(100) 
        self.special_func = False
        self.last_layer_in_queue = None

    def add(self, layer: Layer) -> bool:
        self.layer = layer
        if self.queue.is_full():
            return False
        else:
            self.queue.append(layer)        
            return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        getcolour = start
        if self.queue.is_empty():
            return getcolour
        
        self.last_layer_in_queue = start
        for q in range(self.queue.front , self.queue.rear):
            layer = self.queue.array[q]
            self.last_layer_in_queue = layer.apply(self.last_layer_in_queue,timestamp,x,y)
        return self.last_layer_in_queue
            

    def erase(self, layer: Layer) -> bool:
        self.layer = layer
        if self.queue.is_empty():
            return False
        else:
            self.queue.serve()
            return True

    def special(self):
        my_stack = ArrayStack(len(self.queue)) # used to reverse

        for _ in range(len(self.queue)):
            item = self.queue.serve()
            my_stack.push(item)

        while not my_stack.is_empty():
            item = my_stack.pop()
            if item: # empty string is False in boolean context
                self.queue.append(item)

        """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)  
        """

class SequenceLayerStore(LayerStore):

    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        self.layer = None # sets layer to none hence it starts at default colour 
        self.array_sorted_list = ArraySortedList(1000) 
        self.special_func = False
        self.last_layer = None

    def add(self, layer: Layer) -> bool:
        self.layer = layer
        layers_listItem = ListItem(layer,layer.index)
        self.array_sorted_list.add(layers_listItem)
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        self.layer_listItem = start
        for i in range(0, len(get_layers())-1):
            if self.layer is not None:
                self.last_layer[i] = self.layer.apply(start,timestamp,x,y)
                return self.last_layer
        """
        getcolour = start
        if self.array_sorted_list.is_empty():
            return getcolour
        
        self.last_layer = start
        for index in range(self.array_sorted_list.length):
            layer = self.array_sorted_list.array[index].value
            self.last_layer = layer.apply(self.last_layer,timestamp,x,y)
        return self.last_layer
    
    def erase(self, layer: Layer) -> bool:
        for i in range(self.array_sorted_list.length):
            if not self.array_sorted_list.is_empty():
                if self.array_sorted_list[i].value == layer:
                    self.array_sorted_list.delete_at_index(i)
                    return True

    def special(self):
        self.getcolour = self.last_layer.key
        index = self.array_sorted_list._index_to_add(self.getcolour)
        self.array_sorted_list.delete_at_index(index)
        
        if not self.special_func == None:
            return True