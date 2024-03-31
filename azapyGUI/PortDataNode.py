import json


class PortDataNode:
    def __init__(self, name=None, symbols=None, selectors=None, optimizer=None, 
                 status=None, saved=None, **rest):
        self.name = name if name is not None else "MyPort"
        self.symbols = symbols if symbols is not None else []
        self.selectors = selectors if selectors is not None else {}
        self.optimizer = optimizer if optimizer is not None else {}
        self.status = status if status is not None else "New"
        self.saved = saved if saved is not None else False
        self._active_level = 0
        
        
    def add_optimizer(self, name, param):
        if len(self.optimizer.keys()) > 0: return False
        self.optimizer[name] = {}
        self.optimizer[name]['index'] = 0
        self.optimizer[name]['name'] = name
        self.optimizer[name]['param'] = param
        
        return True
        
    
    def remove_optimizer(self):
        self.optimizer.clear()
        return True
    
    
    def get_optimizer(self):
        ele = self.optimizer.keys()
        if len(ele) == 0: return None
        return self.optimizer[list(ele)[0]]
    
    
    def clear_optimizer(self):
        self.optimizer = {}
        
        
    def update_optimizer(self, param):
        self.optimizer[self.get_optimizer()['name']]['param'] = param
        return True
    
    
    def is_set_optimizer(self):
        return (True if len(self.optimizer.keys()) > 0 else False)
    
    
    def is_set_selector(self, name):
        return (name in self.selectors.keys())
    
    
    def number_selector(self):
        return len(self.selectors.keys())
        
    
    def add_selector(self, name, param):
        if name in self.selectors.keys(): return False
        self.selectors[name] = {}
        self.selectors[name]['index'] = len(self.selectors.keys()) - 1
        self.selectors[name]['name'] = name
        self.selectors[name]['param'] = param
        return True
    
    
    def insert_selector(self, name, param, index):
        kk_sel = self.selectors.keys()
        if index >= len(kk_sel):
            return self.append_selector(name, param)
        for sel in kk_sel:
            if self.selectors[sel]['index'] >= index:
                self.selectors[sel]['index'] += 1 
        self.selectors[name] = {}
        self.selectors[name]['param'] = param
        self.selectors[name]['index'] = index if index >= 0 else 0
        self.selectors[name]['name'] = name
        
        return True
    
    
    def get_selector(self, index_or_name):
        if isinstance(index_or_name, str):
            if index_or_name in self.selectors.keys():
                return self.selectors[index_or_name]
        elif isinstance(index_or_name, int):
            for kk in self.selectors.keys():
                if self.selectors[kk]['index'] == index_or_name:
                    return self.selectors[kk]
        return None
    
    
    def to_list_selector(self):
        if len(self.selectors.keys()) == 0: return []
        return sorted(list(self.selectors.values()), key=lambda x: x['index'])
    
    
    def remove_selector(self, name):
        ele = self.get_selector(name)
        if ele is None: return False
        
        for kk in self.selectors.keys():
            if self.selectors[kk]['index'] > ele['index']:
                self.selectors[kk]['index'] -= 1
        del self.selectors[ele['name']]
        return True
    
    
    def moveUp_selector(self, name):
        index = self.selectors[name]['index']
        if index != 0: 
            nindex = index - 1 
            upname = self.get_selector(nindex)['name']
            self.selectors[upname]['index'] = index
            self.selectors[name]['index'] = nindex
        
        
    def moveDown_selector(self, name):
        index = self.selectors[name]['index']
        if index != self.number_selector() - 1: 
            nindex = index + 1 
            upname = self.get_selector(nindex)['name']
            self.selectors[upname]['index'] = index
            self.selectors[name]['index'] = nindex    
            
            
    def update_selector(self, name, param):
        if name in self.selectors.keys():
            self.selectors[name]['param'] = param
            return True
        return False
            
    
    def add_symbol(self, lsymb):
        if isinstance(lsymb, str):
            self.symbols += [lsymb]
        self.symbols += lsymb
        
        
    def clear_symbol(self):
        self.symbols = []
        
        
    def remove_symbol (self, symb):
        self.symbols.remove(symb)
        
        
    def set_symbol(self, symb):
        self.clear_symbol()
        self.add_symbol(symb)
        
        
    def number_symmbols(self):
        return len(self.symbols)
            
    
    def writeFile(self, file_name):
        fname = file_name
        with open(fname, "w") as write_file:
            json.dump(self.__dict__, write_file)
                
            
    def loadFile(self, file_name):
        fname = file_name
        with open(fname, "r") as read_file:
            data = json.load(read_file)
        self.__init__(**data)
        return self
    
    
    def setActive(self, value=True):
        if value:
            self.status = 'Active'
            self._active_level += 1 
        else:
            if self._active_level > 1:
                self._active_level -= 1 
                return
            self._active_level = 0
            self.status = 'Set'
