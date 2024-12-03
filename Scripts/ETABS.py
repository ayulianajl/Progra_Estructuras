import pandas as pd
import numpy as np
import comtypes.client

class Model:
    
    units_dict = { #Clase para conectar con ETABS y opcionalmente con SAFE. Diccionario de unidades con su valor en la API
        #diccinario de unidades con su valor en la API          
            'kN_mm' : 5,
            'kN_m' : 6,
            'kgf_mm' : 7,
            'kgf_m' : 8,
            'N_mm' : 9,
            'N_m' : 10,
            'tonf_mm' : 11,
            'tonf_m' : 12,
            'kN_cm' : 13,
            'kgf_cm' : 14,
            'N_cm' : 15,
            'tonf_cm' : 16,
    }

    def __init__(self, program = 'ETABS'): #Inicializa una instancia de la clase Model
        if program in {'ETABS', 'etabs', 'Etabs'}:
            self.program = 'ETABS'
            self.connect(self.program)
        elif program in {'SAFE', 'safe', 'Safe'}:
            self.program = 'SAFE'
            self.connect(self.program)
        elif program in {'SAP', 'SAP2000','Sap'}:
            self.program = 'SAP2000'
            self.connect(self.program)
    
    def connect(self, program = 'ETABS'): #Establece una conexión con ETABS utilizando la API COM. 
        try:
            helper = comtypes.client.CreateObject(f'{program}v1.Helper') #Crea un objeto de ayuda para ETABS
            exec(f'helper = helper.QueryInterface(comtypes.gen.{program}v1.cHelper)')
            self.EtabsObject = helper.GetObject(f"CSI.{program}.API.ETABSObject") #Obtiene el objeto ETABS
            self.SapModel = self.EtabsObject.SapModel
            try:
                self.check_connection() #Comprobando una buena conexión a ETABS
            except:
                EtabsObject = comtypes.client.GetActiveObject(f"CSI.{program}.API.ETABSObject") #Si falla, intenta obtener el objeto ETABS activo
                self.ETabsObject = EtabsObject
                self.SapModel = EtabsObject.SapModel
                try:
                    self.check_connection()
                except:
                    raise ConnectionError(f'No es posible la conexión al API de ETABS')
        except:
            raise ConnectionError(f'No es posible la conexión al API de ETABS')
        
    def check_connection(self):
        if self.program in {'ETABS', 'SAFE'}:
            self.set_envelopes_for_display()
        elif self.program in {'SAP2000'}:
            pass
    
    def close(self):
        '''
        Cerrar 
        
        '''
        SapModel,EtabsObject = self.SapModel,self.ETabsObject
        SapModel.SetModelIsLocked(False) #En caso de que esté bloqueado, esta línea de código lo desbloquea.
        EtabsObject.ApplicationExit(True) #Con esta línea de código cerramos la aplicación. 
        self.SapModel = None
        self.ETabsObject = None
    
    def set_units(self,unit,SAFE=False):
        '''
        Definir unidades de trabajo solo para el output del código
        imput: 
        unit: Unidad definida en el diccionario: units_dict
        '''
        if SAFE:
            SapModel = self.SapModelSafe
        else:
            SapModel = self.SapModel
        SapModel.SetPresentUnits(self.units_dict[unit])

    def set_envelopes_for_display(self,set_envelopes = True,SAFE = False):
        '''
        Método de formateo de tablas (por defecto elige envolventes en casos de carga compuesto)
        
        '''
        if SAFE:
            SapModel = self.SapModelSafe
        else:
            SapModel = self.SapModel
        IsUserBaseReactionLocation = False
        UserBaseReactionX = 0
        UserBaseReactionY = 0
        UserBaseReactionZ = 0
        IsAllModes = True
        StartMode = 0
        EndMode = 0
        IsAllBucklingModes = True
        StartBucklingMode= 0
        EndBucklingMode = 0
        MultistepStatic = 1 if set_envelopes else 2
        NonlinearStatic = 1 if set_envelopes else 2
        ModalHistory = 1
        DirectHistory = 1
        Combo = 2
        SapModel.DataBaseTables.SetOutputOptionsForDisplay(
            IsUserBaseReactionLocation,UserBaseReactionX,UserBaseReactionY,UserBaseReactionZ,IsAllModes,StartMode,EndMode,IsAllBucklingModes,StartBucklingMode,EndBucklingMode,MultistepStatic,NonlinearStatic,ModalHistory ,
        DirectHistory ,
        Combo ,
        ) 

    def get_table(self, table_name, set_envelopes = True, SAFE = False):
        '''
        Método de extracción de tablas, usa envolventes por defecto. Corre el modelo en caso de encontrar datos
        
        '''
        if SAFE:
            SapModel = self.SapModelSafe
        else:
            SapModel = self.SapModel
        
        self.set_envelopes_for_display(set_envelopes = set_envelopes, SAFE = SAFE)
        data = SapModel.DatabaseTables.GetTableForDisplayArray(table_name, FieldKeyList = '', GroupName = '')

        if not data[2][0]: #En el caso de que no esté corrido el programa, esta línea de comando corre el programa.
            SapModel.Analyze.RunAnalysis()
            data = SapModel.DatabaseTables.GetTableForDisplayArray(table_name, FieldKeyList = '', GroupName = '')
        
        columns = data[2] #data es una lista en la que la posición 2 son las columnas de nuestra tabla de interés. 
        data = [i if i else '' for i in data[4]] #Reemplazando valores None por ''. La posición 4 de la lista data, son todos los valores de nuestra tabla de interés. 
        #reshape data
        data = pd.DataFrame(data) 
        data = data.values.reshape(int(len(data)/len(columns)),len(columns)) #Está linea de código ordena los datos de la lista data en una tabla que se puede leer adecuadamente. len(data)/len(columnas) es la cantidad de filas y len(columnas) es la cantidad de columnas.
        table = pd.DataFrame(data, columns = columns) #La línea anterior convierte los datos en un array. Se necesita volver a convertirlos en un Data Frame.      
        return table
    

if __name__ == '__main__':
    m_etabs = Model()
    print(m_etabs.get_table('Modal Participating Mass Ratios'))

