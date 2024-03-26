from abc import ABCMeta, abstractmethod
from enum import Enum

######################################################## INTRODUCCIÓN ##############################################################

#En el planteamiento que hemos hecho para resolver el problema, tenemos una clase abstracta Persona de la que heredan las clases Estudiante, ProfesorAsociado 
#e Investigador. La clase persona es la encargada de 'guardar' los atributos más `personales` de sus clases derivadas, como son el nombre, el dni, la direccion o el sexo.
#Además también creamos otra clase abstracta llamada MiembroDepartamento de la que heredan ProfesorAsociado e Investigador, dándose entonces herencia múltiple.
#Esta segunda clase abstracta nos sirve para 'guardar' aquellos atributos más 'institucionales', própios únicamente de aquellas personas que trabajan en la universidad, 
#como profesores o investigadores.Del enunciado entendemos que cualquier profesor o investigador debe pertenecer a un departamento, y solo a uno.
#Cabe destacar también que dado que los profesores que son titulares, son a su vez también investigadores, creímos conveniente que de la clase Investigador, heredase la clase 
#ProfesorTitular. Es decir las clases Investigador y ProfesorAsociado presentan herencia múltiple de Persona y MiembroDepartamento, y luego a su vez la clase Investigador 
#presenta como clase derivada a ProfesorTitular.
#Por último para poder dar lugar a una gestión centralizada de todas las clases y sus respectivas instancias, implementamos una clase Universidad, que pudiera añadir y eliminar
#tanto alumnos como miembros de los departamentos, así como asignaturas. A la vez que otras funcionalidades como matricular a los alumnos en algunas asignaturas, o cambiar
#de Departamento a cualquier miembro.
#Así conseguimos dar forma a todos los aspectos requeridos en el pdf.






########################################################## EXCEPCIONES ############################################################


#Aqui se definen las Excepciones que se emplean para el manejo de los errores.
#Principalmente preocupa el paso de atributos no válidos, al no ser el mismo tipo de dato que el parámetro que espera recibir el método.
#También resulta relevante evitar que en el sistema de la Universidad hayan datos repetidos, o que se intente llevar a cabo alguna operación
#con algún objeto que no se encuentre en el sistema.

class DepartamentoError(Exception):         
    def __init__(self, mensaje= "Error: Departamento Pasado No válido"):
        self.message = mensaje
        super().__init__(self.message)


class ExistingInformationError(Exception):
    def __init__(self, mensaje= "Error: Información ya existente en el Sistema"):
        self.message = mensaje
        super().__init__(self.message)


class NotValidType(Exception):
    def __init__(self, mensaje="Error: El tipo proporcionado no es válido"):
        self.message = mensaje
        super().__init__(self.message)

class IdentifierError(Exception):
    def __init__(self, mensaje="Error: El Identificador proporcionado no es válido"):
        self.message = mensaje
        super().__init__(self.message)




############################################################ ENUMERACIONES #################################################################

#Creamos las enumeraciones que empleamos.
#Cabe mencionar que la enumeración TipoMiembro, la creamos con la idea de distinguir entre si un profesor es 
#asociado titular. De forma que internamente en el sistema no tengamos que emplear estructuras de datos distintas 
#para almacenarlos, sino una única conjunta.


class TipoMiembro(Enum):
    Investigador    = 1
    Asociado        = 2
    Titular         = 3

class Sexo(Enum):
    Masculino   = 1
    Femenino    = 2

class AreaInvestigacion(Enum):  
    InvestigacionOperativa          = 1
    ArquitecturaDeComputadores      = 2
    AprendizajeMaquina              = 3
    AprendizajeProfundo             = 4
    ComputacionAltasPrestaciones    = 5
    Software                        = 6

class Departamento(Enum):   
    DIIC = 1
    DITEC = 2
    DIS = 3


############################################# DEFINICIÓN DE LAS CLASES #####################################################################


#CLASE PERSONA
    #
    #LA CLASE PERSONA ES UNA CLASE ABSTRACTA, QUE FUERZA A SUS CLASES DERIVADAS (Estudiante, ProfesorAsociado, Investigador)
    #a implementar el método devooverDatos().
    #También realiza una labor importante al comprobar que el sexo y el dni de la persona sen del formato correcto

class Persona(metaclass = ABCMeta):             
    def __init__(self, nombre : str, direccion : str ,  dni : str, sexo: Sexo):

        if not isinstance(sexo, Sexo): raise NotValidType("Error: El atributo sexo debe ser una instancia de la clase Sexo")
        if not isinstance(dni, str): raise NotValidType("El tipo de dato dni, no es correcto")
        
        self.nombre = nombre
        self._dni = dni
        self._sexo = sexo
        self._direccion = direccion

    @abstractmethod
    def devolverDatos(self):
        pass




#CLASE MIEMBRODEPARTAMENTO
    #
    # Al igual que la clase Persona, la clase MiembroDepartaemnto tambien es abstracta y fuerza a sus clases derivadas (ProfesorASociado, ProfesorTitular e Investigador)
    # a implementar el método devolverDatos. Pensamos que lo correcto sería que fuese una clase abstracta ya que no tiene sentido que se pueda instanciar.
    # Esta clase recoge los atributos propios de aquellas instancias que simulan a trabajadores de la Universidad. 
    # Los aributos que recibe son comprobados para evitar tipos de datos incorrectos, en caso de que lo sean salta la excepción pertinente.
    # Además esta clase implementa otros métodos que son heredados por sus clases derivadas y permiten llevar a cabo el cambio de departamento de los
    # miembros. De forma que se implementa una sola vez y las clases ProfesorTitular, Investigador y ProfesorAsociado lo pueden heredar.
    
class MiembroDepartamento(metaclass = ABCMeta):          
    def __init__(self, identificador: str, tipo: TipoMiembro, departamento:Departamento):

        if not isinstance(tipo, TipoMiembro): raise NotValidType("Error: El atributo tipo debe ser una instacia de la clase Tipomiembro")
        if not isinstance(departamento, Departamento): raise DepartamentoError()
        if not isinstance(identificador, str): raise NotValidType("Error: El identificador pasado no es válido")

        self.ID = identificador
        self.tipo = tipo
        self._departamento = departamento
            
    @abstractmethod
    def devolverDatos(self):
        pass        
    
    def devolverDepartamento(self):
        return self._departamento
    
    def cambioDepartamento(self, nuevo_departamento):

        if not isinstance(nuevo_departamento, Departamento):
            raise DepartamentoError()
        
        self._departamento = nuevo_departamento



#CLASE ASIGNATURA
    #
    # La clase asignatura permite la instanciación de asignaturas, de forma que queden en un mismo objetos recogidas todas las características de una asignatura.
    # También se nos ocurrió aplicar el concepto de atributos de clase añadiendole un atributo que guarda el precio del crédito,  
    # lo que me permite el cálculo del precio de la asignatura en función de los créditos de esta.
    # Los aributos que recibe son comprobados para evitar tipos de datos incorrectos, en caso de que lo sean salta la excepción pertinente.

class Asignatura:
    precio_credito = 16.5

    def __init__(self, nombre: str, codigo_asignatura : str, creditos: float, carrera : str, departamento : Departamento, curso: int):

        if not isinstance(departamento, Departamento): raise DepartamentoError()
        if not isinstance(creditos, float) and not isinstance(creditos, int): NotValidType("Error: Los créditos deben ser un numero entero o decimal")

        self.nombre = nombre
        self.codigo_asignatura = codigo_asignatura
        self.creditos = creditos
        self.carrera = carrera
        self._departamento = departamento
        self.curso = curso

    def devolverDepartamento(self):
        return self._departamento

    def __str__(self):
        return f"Nombre: {self.nombre}, Código asignatura: {self.codigo_asignatura} , Creditos: {self.creditos}, Carrera: {self.carrera}, Deparatamento: {self._departamento.name}, Curso: {self.curso}, Precio: {Asignatura.precio_credito * self.creditos}"
    

#CLASE ESTUDIANTE
    #
    # La clase estudiante hereda de la clase persona, y además implementa dos atributos más, que son el número de expediente, clave que emplearemos
    # para buscar al estudiante en el sistema gestor de la universidad, y un listado de asignaturas en las que el estudiante estña matriculado.
    # Inicialmente al isntanciar un objeto Estudiante, el listado de las asignaturas en las que está matriculado está vacío. Solo se añaden asignaturas 
    # a dicho listado si el sistema gestor de la universidad matricula al alumno en una de ellas.
    # El listado de asignaturas del estudiante es un atributo privado, por lo que su modificación solo es a traves de dos métodos matricular y desmatricular (getters)
    # También hay dos métodos setters para este listado de asignaturas, uno que permite imprimir las asignaturas del listado por pantalla (mostrar_asignaturas()),
    # y otro que devuelve el listado, con fines de comprobación de que la asignatura está en el listado.



class Estudiante(Persona):
    def __init__(self, nombre: str, direccion: str, dni: str, numero_expediente:str, sexo: Sexo):
        super().__init__(nombre, direccion, dni, sexo)
        self.numero_expediente = numero_expediente
        self.__listado_asignaturas = []
    
    def devolverDatos(self):                       
        return f"Nombre : {self.nombre}, Dni: {self._dni}, Direccion : {self._direccion}, Sexo : {self._sexo.name}" + f", Número de Expediente : {self.numero_expediente}, Rol : Estudiante"
    
    def __str__(self):
        return f"{self.devolverDatos()}"

    def matricular(self, asignatura :Asignatura):
        self.__listado_asignaturas.append(asignatura)

    def desmatricular(self, asignatura):
        self.__listado_asignaturas.remove(asignatura)

    def mostrar_asignaturas(self):
        for a in self.__listado_asignaturas:
            print(a)
    
    def asignaturas(self):
        return self.__listado_asignaturas

    def devolverDni(self):
        return self._dni


#CLASE PROFESORASOCIADO
    #
    # La clase profesor asociado presenta herencia múltiple, siendo una clase derivada tanto de la clase Persona como de la clase MiembroDepartamento.
    # Al igual que en los estudiantes, todos los miembros de la Universidad (MiembroDepartamento), presentan un identificador que permite su identificación dentro del 
    # sistema de la Universidad. También presentan un listado de asignaturas a las que está vinculado el profesor. Este listado de asignaturas
    # es privado, por lo que para su obtención y modificación se emplean métodos getters y setters.


class ProfesorAsociado(Persona, MiembroDepartamento):
    def __init__(self, nombre: str, direccion: str, dni: str, identificador:str, sexo: Sexo, tipo: TipoMiembro, departamento: Departamento):
        Persona.__init__(self, nombre, direccion, dni, sexo)
        MiembroDepartamento.__init__(self,identificador, tipo, departamento)
        self.__listado_asignaturas = []

    def devolverDatos(self):   
        return f"Nombre : {self.nombre}, Dni: {self._dni}, Direccion : {self._direccion}, Sexo : {self._sexo.name}, Identificador : {self.ID}, Miembro: {self.tipo.name}, Departamento: {self._departamento.name}"

    def __str__(self):
        return f"{self.devolverDatos()}"
    
    def incorporar_asignatura(self, asignatura :Asignatura):
        self.__listado_asignaturas.append(asignatura)

    def eliminar_asignatura(self, asignatura : Asignatura):
        self.__listado_asignaturas.remove(asignatura)
    
    def asignaturas(self):
        return self.__listado_asignaturas
    
    def mostrar_asignaturas(self):
        for a in self.__listado_asignaturas:
            print(a)

    def devolverDni(self):
        return self._dni
    


#CLASE INVESTIGADOR
    #
    # La clase investigador presenta herencia múltiple, siendo una clase derivada tanto de la clase Persona como de la clase MiembroDepartamento.
    # Presenta como atributo un identificador, que hereda de MiembroDepartamento, y permite su identificación dentro del sistema de la Universidad.
    # Además tiene un atributo que indica cual es su Área de Investigación, este atributo debe ser una instancia de la enumeración AreaInvestigación
    # por lo que dicho atributo es comprobado. En caso de no ser del tipo AreaInvestigación salta una excepción.
    # Cabe detacar también la implementación del método especial o mágino, __str__, que permite redefinir la impresión por pantalla de las instancias de ese método.
    # Y como ya existe el método devolverDatos, lo que hace este método mágico es tan solo llamar a es devolverDatos(), que es método que devuelve una
    # cadena de caracteres los atributos del objeto.
    
   
    

class Investigador(Persona, MiembroDepartamento):
    def __init__(self, nombre: str, direccion: str, dni: str, identificador:str, sexo: Sexo, tipo:TipoMiembro,  departamento:Departamento, area_investigacion : AreaInvestigacion):
        Persona.__init__(self, nombre, direccion, dni, sexo)
        MiembroDepartamento.__init__(self, identificador, tipo, departamento)

        if not isinstance(area_investigacion, AreaInvestigacion): raise NotValidType()

        self.area_investigacion = area_investigacion

    def devolverDatos(self):   
        return  f"Nombre : {self.nombre}, Dni: {self._dni}, Direccion : {self._direccion}, Sexo : {self._sexo.name}, Identificador : {self.ID}, Miembro: {self.tipo.name}, Departamento: {self._departamento.name}, Área Investigación : {self.area_investigacion.name}"
    
    def __str__(self):
        return f"{self.devolverDatos()}"
    
    def devolverDni(self):
        return self._dni


#CLASE PROFESORASOCIADO
    #
    # La clase profesor titular es una clase derivada de la clase Investigador, la cual hereda a su vez de las clases Persona y MimebroDepartamento.
    # Presenta un identificador al igual que todos los miembros de la Universidad (MiembroDepartamento), permitiendo su identificación en el sistema 
    # También presentan un listado de asignaturas a las que está vinculado el profesor. 
    # Este listado de asignaturas es privado, por lo que para su obtención y modificación se emplean métodos getters y setters.


class ProfesorTitular(Investigador):
    def __init__(self, nombre: str, direccion: str, dni: str, identificador:str, sexo: Sexo, tipo:TipoMiembro, departamento : Departamento, area_investigacion : AreaInvestigacion):

        super().__init__(nombre, direccion, dni, identificador,sexo, tipo, departamento, area_investigacion)
        self.__listado_asignaturas = []


    def devolverDatos(self):
        return super().devolverDatos()
    
    def __str__(self):
        return f"{self.devolverDatos()}"
    
    def incorporar_asignatura(self, asignatura :Asignatura):
        self.__listado_asignaturas.append(asignatura)

    def eliminar_asignatura(self, asignatura : Asignatura):
        self.__listado_asignaturas.remove(asignatura)

    def asignaturas(self):
        return self.__listado_asignaturas

    def mostrar_asignaturas(self):
        for a in self.__listado_asignaturas:
            print(a)    

    def devolverDni(self):
        return self._dni
    


#CLASE UNIVERSIDAD
    #
    # La clase Universidad permite gestionar las funcionalidades propias de la universidad, añadiendo estudiantes, profesores, investigadores,
    # y asignaturas, así como borrandolos o mostrandolos. También lleva a cabo otras operaciones como matricular y desmatricular alumnos o vincular 
    # y desvincular profesores a una asignatura en concreto.
    # Es importante remarcar su estructura interna. La clase universidad presenta diccionarios para guardar a los objetos con los que trabaja.
    # Tiene un único diccionario para los profesores, independiendientemente del tipo que sean, bien titulares o bien asociados, de ahí el atributo tipo
    # que heredan tanto profesores como investigadores de la clase MiembroDepartamento. Este diccionario que guarda a los profesores que se incorporan a la universidad
    # se llama listado_profesores.
    # De la misma forma emplea un diccionario para las asignaturas, los investigadores y los estudiantes.
    # El motivo de emplear diccionarios en vez de una lista para guardar lo objetos es, que su estructura clave:valor, evita tener que emplear bucles
    # for e ir comparando por un atributo para buscar un obejto objeto. Las claves en estos diccionarios son los propios atributos identificador, numero_expediente o 
    # código, de los profesores o investigadores, estudiantes y asignaturas respectivamente. 
    # De esta forma el gestor debe buscar a un objeto por dicho identificador, numerro de expediente o código, que son únicos, y no por su nombre que puede estar repetido,
    # o por su dni, en caso de ser una persona, dato que consideramos sensible y que debe ser privado. 
    # Al ser únicos estos atributos, hemos tenido que implementar ciertos manejos de excepciones que permitan identificar cuando se está desantendiendo a esta característica,
    # como por ejemplo, no se puede añadir un profesor con un identificador que ya esté en uso, por lo que antes de crearse la instancia que representa al profesor, se
    # comprueba que el identificador no sea ya una clave del diccionario.

#Funcionalidades:
    #
    # MÉTODOS DE INCORPORACIÓN Y ELIMINACIÓN:
    # Entre los métodos que implementa la clase Universidad, hay métodos que permiten la incorporación y eliminación de los estudiantes, asignaturas y los miembros de Departamentos, que son
    # los investigadores y los profesores. Estos métodos que incorporan nuevos objetos al sistema, primero comprueban que no haya ya un objeto usando un identificador, código o numero de expediente, 
    # que ya haya sido asignado a un objeto, y tras esto, en caso de ser una persona,  hace una segunda comprobación de que no hay un objeto ya guardado con igual dni. Ya que podría darse
    # el caso de estar guardando a la misma persona con dos identificadores distintos. Y finalmente, si ha pasado las comprobaciones se crea una nueva instancia,
    # que se guardará en el diccionario correspondiente.
    # Los métodos de eliminación, requieren del paso como argumento del identificador, código o numero de expediente del objeto a eliminar, de forma que, al ser esta la clave
    # del objeto en el diccionario, solo tienen que aplicar el borrado. En estos métodos la comprobación consiste en ver que el objeto a eliminar existe verdaderamente en el sistema.
    # (comprobar que el identificador buscado está entre las claves de los diccionarios).
    # Es importante destacar que si se elimina una asignatura, esta también se borra de la lista de asiganturas de todos los estudiantes que estaban matriculados en ella
    # así como del listado de asignaturas a las que está vinculado el profesor o profesores que la impartían.
    #
    # MÉTODOS PARA MOSTRAR POR PANTALLA
    # Estos métodos cuyo nombre empiezan por la palabra mostrar, son métodos que recorrer el diccionario correspondiente para imprimir por pantalla toddos los objetos de dicho diccionario.
    # También los hay algo más específicos como el de mostrar_profesores_asociados, que recorren todo el diccionario de profesores pero filtrando por el atributo tipo,
    # para solo imprimir por pantalla los asociados. 
    # Y en el caso de las asignaturas, para mostrarlas, se muestran por departamento, es decir, el método obtiene como parámetro el Departamento del que debe listar sus
    # asiganturas. Por lo que debe iterar al diccionario que guarda las asiganturas y comparar para cada una de ellas el atributo departamento, imprimiendo por pantalla solo aquellas
    # cuyo atributo departamento coincida con el departamento especificado.
    #
    #
    # MÉTODOS PARA VICULAR Y DESVINCULAR A UN PROFESOR O A UN ESTUDIANTE CON UNA ASIGNATURA.
    # Estos métodos como son matricular, desmatricular o vincularProfesorAsignatura y desvincularProfesorAsignatura, requiren del paso del identificador del profesor o numero
    # de expediente del estudiante, junto con el código de la asignatura.
    # Primeramente lo que hacen es comprobar que existan tanto la asignatura como el profesor o estudiante, para ello se sirven de unos métodos auxilares que enmascaran esta 
    # búsqueda, como son devolverMiembro() para encontrar a los profesores, devolverEstudiante para los Estudiantes, y devolverAasignatura para las Asignaturas. Estos métods auxiliares
    # lo que hacen es comprobar que el identificador o código pasado existe en el diccionario correspondiente y devolverlo, pero si no lo encuentran devolverán un None.
    # Si se recibe un None saltará una excepción indicando bien que el identificador, código de asignatura o numero de expediente no es válido. 
    # Pero si tanto la asignatura como el profesor o estudiante son encontrados, al objeto profesor o estudiante se le añade a su listado de asignaturas la nueva asignatura. O en caso de ser
    # el método de desvincular o desmatricular, la asignatura es eliminada del listado de asignaturas del profesor o estudiante.
    #
    #
    # OTRAS FUNIONALIDADES.
    # Cabe destacar el método cambiarDepartamento(), al cual se le debe pasar el identificador del miembro, es decir, investigador o profesor, junto con el nuevo departamento.
    # Internamente el método lo que hace es acceder al atributo departamento del profesor o investigador y cambiarlo. Para ello previamente ha comprobado que el identificador pasado
    # realmente está asociado a un objeto guardado en el sistema, y que el nuevo departamento es una instancia de la enumeración Departamento, además de comprobar que el nuevo departamento
    # no es el mismo que en el que ya estaba previamente el miembro.
    # 
    # También hemos implementado un método adicional calcularMatricula() que permite calcular el precio total de la matricula de un alumno en función del número de asigaturas a las que esté matriculado
    # y del número de créditos de estas. Para ello la clase Asigantura presenta un atributo de clase que indica el precio del crédito, teniendo solo que multiplicarlo 
    # por el número de créditos para obtener el precio de cada asigantura.

    



class Universidad:
    def __init__(self, nombre : str, direccion: str):
        self.nombre = nombre
        self.direccion = direccion
        self.__listado_estudiantes = {}
        self.__listado_asignaturas = {}
        self.__listado_profesores  = {}
        self.__listado_investigadores = {}

    # Métodos que permiten devolver un objeto guardado en el sistema, ya sea profesor, investigador, asignatura o estudiante. Se les debe pasar el identificador, código 
    # o número de expediente del objeto que buscan.

    def devolverMiembro(self, identificador):      
        if identificador in self.__listado_profesores:
            return self.__listado_profesores[identificador]
        if identificador in self.__listado_investigadores:
            return self.__listado_investigadores[identificador]
        return None 

    def devolverEstudiante(self, numero_expediente):   #Ok
        if numero_expediente not in self.__listado_estudiantes:
            return None 
        return self.__listado_estudiantes[numero_expediente]

    def devolverAsignatura(self, codigo_asignatura):    #Ok
        if codigo_asignatura not in self.__listado_asignaturas:
            return None 
        return self.__listado_asignaturas[codigo_asignatura]
        

    def incorporar_estudiante(self, nombre_estudiante, direccion, dni, numero_expediente, sexo):          #OK
        #Se hace una primera comprobación de que el usuario No ha sido todavía añadido a la Universidad

        if numero_expediente in self.__listado_estudiantes:
            raise IdentifierError("Error: El número de expediente indicado está asociado a otro estudiante. Por favor cambie el identificador, debe ser único")
        
        #Se hace una segunda comprobación 
        for e in self.__listado_estudiantes:
            es = self.__listado_estudiantes[e]
            if es.devolverDni() == dni:
                raise ExistingInformationError("Error: Estudiante con dni ya añadido")
                
            

        
        self.__listado_estudiantes[numero_expediente] = Estudiante(nombre_estudiante, direccion, dni, numero_expediente, sexo)                                           


    def incorporar_profesor(self, nombre, direccion, dni, identificador, sexo, tipo, departamento, area_investigacion = None): #OK, habría que comporbar que el tipo indicado es asociado o titular

        if identificador in self.__listado_profesores:
            raise IdentifierError("Error: Identificador escogido está en uso. Por favor cambie el identificador, debe ser único")
             

        for id in self.__listado_profesores:
            if self.__listado_profesores[id].devolverDni() == dni:
                raise ExistingInformationError("Error: Profesor ya añadido")

        
        if tipo.value == 2:
            profesor = ProfesorAsociado(nombre, direccion, dni, identificador, sexo, tipo, departamento)
        if tipo.value == 3:
            profesor = ProfesorTitular(nombre, direccion, dni, identificador, sexo, tipo, departamento, area_investigacion)

        self.__listado_profesores[identificador] = profesor

    
    def incorporar_investigador(self, nombre, direccion, dni, identificador, sexo, departamento, area_investigacion): #OK , habría que comprobar que el tipo indicado es investigador
        
        if identificador in self.__listado_investigadores:
            raise IdentifierError("Error: Identificador escogido está en uso. Por favor cambie el identificador, debe ser único")          


        for id in self.__listado_investigadores:
            if self.__listado_investigadores[id].devolverDni() == dni:
                raise ExistingInformationError("Error: Investigador ya añadido")
            
        
        
        self.__listado_investigadores[identificador] = Investigador(nombre, direccion, dni, identificador, sexo, TipoMiembro.Investigador, departamento, area_investigacion)

    
    def incorporar_asignatura(self, nombre, codigo_asignatura, creditos, carrera, curso, departamento): #OK

        if codigo_asignatura in self.__listado_asignaturas:
            raise ExistingInformationError("Error: Asignatura ya añadida")
             

        self.__listado_asignaturas[codigo_asignatura] = Asignatura(nombre, codigo_asignatura, creditos, carrera, departamento, curso)


    def mostrar_estudiantes(self):  #OK
        print("Estudiantes dados de alta:")
        for id in self.__listado_estudiantes:
            print(self.__listado_estudiantes[id])


    def mostrar_investigadores(self):   #OK
        for investigador in self.__listado_investigadores:
            print(self.__listado_investigadores[investigador])

    
    def mostrar_profesores_titulares(self): #Ok
        for profesor in self.__listado_profesores:
            if self.__listado_profesores[profesor].tipo == TipoMiembro.Titular:
                print(self.__listado_profesores[profesor])

    def mostrar_profesores_asociados(self): #Ok
        for profesor in self.__listado_profesores:
            if self.__listado_profesores[profesor].tipo == TipoMiembro.Asociado:
                print(self.__listado_profesores[profesor])
            
    def mostrar_profesores(self):       #OK
        for profesor in self.__listado_profesores:
                print(self.__listado_profesores[profesor])


    def mostrar_asignaturas_departamento(self, departamento):   #OK
        if not isinstance(departamento, Departamento):
            raise DepartamentoError()
            
        
        for asignatura in self.__listado_asignaturas:
            if self.__listado_asignaturas[asignatura].devolverDepartamento() == departamento:
                print(self.__listado_asignaturas[asignatura])
            

    def mostrar_miembros_departamento(self, departamento):  #OK
        if not isinstance(departamento, Departamento):
            raise DepartamentoError()
            
        
        print("Investigadores")
        for investigador in self.__listado_investigadores:
            if self.__listado_investigadores[investigador].devolverDepartamento() == departamento:
                print(self.__listado_investigadores[investigador])

        print("Profesores")
        for profesor in self.__listado_profesores:
            if self.__listado_profesores[profesor].devolverDepartamento() == departamento:
                print(self.__listado_profesores[profesor])
        

        
    def eliminar_estudiante(self, identificador):   #OK

        if identificador not in self.__listado_estudiantes: 
            raise IdentifierError("Error: Estudiante No encontrado")   
                                                                                                                      
        del self.__listado_estudiantes[identificador]                                                                   


    def eliminar_miembro(self, identificador):          #OK

        if identificador in self.__listado_investigadores:
           del self.__listado_investigadores[identificador]
           return
        if identificador in self.__listado_profesores:
            del self.__listado_profesores[identificador]
            return

        raise IdentifierError("Error:Miembro No encontrado")



    def eliminar_asignatura(self, codigo_asignatura):       #Ok

        if codigo_asignatura not in self.__listado_asignaturas:
            raise IdentifierError("Error: Asignatura No encontrada")
            
        
        asignatura = self.devolverAsignatura(codigo_asignatura)

        del self.__listado_asignaturas[codigo_asignatura]

        #Si hay un estudiante matriculado en la asignatura que quiero eliminar, he de desmatricular al estudiante
        for numero_expediente in self.__listado_estudiantes:
            estudiante = self.__listado_estudiantes[numero_expediente]
            if asignatura in estudiante.asignaturas():
                estudiante.desmatricular(asignatura)

        #Al eliminar la asignatura todo aquel profesor que la impartiese debe dejar de impartirla
        for identificador in self.__listado_profesores:
            profesor = self.__listado_profesores[identificador]
            if asignatura in profesor.asignaturas():
                profesor.eliminar_asignatura(asignatura)
            


    def cambiarDepartamento(self, identificador_miembro, nuevo_departamento):       #OK

        if not isinstance(nuevo_departamento, Departamento): raise DepartamentoError()

        miembro = self.devolverMiembro(identificador_miembro)
        if miembro is None:
            raise IdentifierError("Error: Miembro no encontrado")

        if miembro.devolverDepartamento() == nuevo_departamento:
            raise ExistingInformationError("Error: El individuo ya se encuentra en el departamento")
            
        
        miembro.cambioDepartamento(nuevo_departamento) 
      


    def matricular(self, codigo_asignatura, identificador_estudiante):       #OK
        asignatura = self.devolverAsignatura(codigo_asignatura)
        if asignatura is None: 
            raise IdentifierError("Error: La asignatura no existe")
        
        estudiante = self.devolverEstudiante(identificador_estudiante)
        if estudiante is None:
            raise IdentifierError("Error: El estudiante no existe")
        
        estudiante.matricular(asignatura)

    
    def desmatricular(self, codigo_asignatura, identificador_estudiante):       #OK
        asignatura = self.devolverAsignatura(codigo_asignatura)
        if asignatura is None:
            raise IdentifierError("Error: La asignatura no existe")
        
        estudiante = self.devolverEstudiante(identificador_estudiante)
        if estudiante is None:
            raise IdentifierError("Error: El estudiante no existe")
        
        if asignatura not in estudiante.asignaturas():
            raise IdentifierError("Error: El estudiante seleccionado No está matriculado esa asignatura")
            
        
        estudiante.desmatricular(asignatura)



    def vincularProfesorAsignatura(self, codigo_asignatura, identificador_profesor):        #Ok

        asignatura = self.devolverAsignatura(codigo_asignatura)
        if asignatura is None:
            raise IdentifierError("Error: La asignatura no existe")
        
        profesor = self.devolverMiembro(identificador_profesor)
        if profesor is None:
            raise IdentifierError("Error: El profesor no existe")
        
        if asignatura in profesor.asignaturas():
            raise ExistingInformationError("Error: El profesor ya está vinculado a esa asignatura")
        
        profesor.incorporar_asignatura(asignatura)
        

    def desvincularProfesorAsignatura(self, codigo_asignatura, identificador_profesor):       #Ok

        asignatura = self.devolverAsignatura(codigo_asignatura)
        if asignatura is None:
            raise IdentifierError("Error: La asignatura no existe")
        
        profesor = self.devolverMiembro(identificador_profesor)
        if profesor is None:
            raise IdentifierError("Error: El profesor no existe")
        
        if asignatura not in profesor.asignaturas():
            raise ExistingInformationError("Error: El profesor seleccionado No está asociado a esa asignatura")
             
        profesor.eliminar_asignatura(asignatura)


    def cambiarIdentificador(self, identificador, nuevo_identificador): #OK
        miembro = self.devolverMiembro(identificador)
        if miembro is None:
            raise IdentifierError("Error: El miembro no existe")
        
        miembro.ID = nuevo_identificador
        self.eliminar_miembro(identificador)

        if miembro.tipo == TipoMiembro.Investigador:
            self.__listado_investigadores[nuevo_identificador] = miembro
        else:
            self.__listado_profesores[nuevo_identificador] = miembro

    
    def cambiarNumeroExpediente(self, numero_expediente, nuevo_numero_expediente):  #OK
        estudiante = self.devolverEstudiante(numero_expediente)
        if estudiante is None:
            raise IdentifierError("Error: El estudiante no existe")
        
        estudiante.numero_expediente = nuevo_numero_expediente
        self.eliminar_estudiante(numero_expediente)
        self.__listado_estudiantes[nuevo_numero_expediente] = estudiante
        


    def cambiarCodigoAsignatura(self, codigo, codigo_nuevo):        #OK
        asignatura = self.devolverAsignatura(codigo)
        if asignatura is None:
            raise IdentifierError("Error: La asignatura indicada no existe") 
        
        asignatura.codigo_asignatura = codigo_nuevo
        self.eliminar_asignatura(codigo)
        self.__listado_asignaturas[codigo_nuevo] = asignatura




    def calcularMatricula(self, numero_expediente):     #OK
        total = 0
        estudiante = self.devolverEstudiante(numero_expediente)
        if estudiante is None:
            raise IdentifierError("Error: El estudiante no existe")
        
        for a in estudiante.asignaturas():
            total += Asignatura.precio_credito * a.creditos

        print(f"Total: {total}")



def test_incorporar_estudiante():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    sexo = Sexo.Masculino  # Usando el objeto de la enumeración Sexo correspondiente
    universidad.incorporar_estudiante("Nombre Estudiante", "Dirección Estudiante", "12345678A", "123", sexo)
    estudiante = universidad.devolverEstudiante("123")
    assert estudiante is not None
    assert estudiante.nombre == "Nombre Estudiante"


def test_incorporar_profesor():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_profesor("Jorge Larrey", "Calle Olmo", "54328-B", "a-4356", Sexo.Masculino, TipoMiembro.Asociado, Departamento.DIIC)
    profesor = universidad.devolverMiembro("a-4356")
    assert profesor is not None
    assert profesor.nombre == "Jorge Larrey"

def test_incorporar_investigador():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    sexo = Sexo.Masculino
    departamento = Departamento.DIS
    universidad.incorporar_investigador("Nombre Investigador", "Dirección Investigador", "55555555X", "789", sexo, departamento, AreaInvestigacion.InvestigacionOperativa)
    investigador = universidad.devolverMiembro("789")
    assert investigador is not None
    assert investigador.nombre == "Nombre Investigador"

def test_incorporar_asignatura():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_asignatura("Nombre Asignatura", "COD123", 6, "Carrera", 2, Departamento.DIIC)
    asignatura = universidad.devolverAsignatura("COD123")
    assert asignatura is not None
    assert asignatura.nombre == "Nombre Asignatura"

def test_mostrar_asignaturas_departamento(capfd):
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_asignatura("Nombre Asignatura", "COD123", 6, "Carrera", 2, Departamento.DIIC)
    universidad.mostrar_asignaturas_departamento(Departamento.DIIC)
    out, _ = capfd.readouterr()
    assert "Nombre Asignatura" in out

def test_matricular():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_estudiante("Nombre Estudiante", "Dirección Estudiante", "12345678A", "123", Sexo.Masculino)
    universidad.incorporar_asignatura("Nombre Asignatura", "COD123", 6, "Carrera", 2, Departamento.DIIC)
    universidad.matricular("COD123", "123")
    estudiante = universidad.devolverEstudiante("123")
    assert len(estudiante.asignaturas()) == 1

def test_desmatricular():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_estudiante("Nombre Estudiante", "Dirección Estudiante", "12345678A", "123", Sexo.Masculino)
    universidad.incorporar_asignatura("Nombre Asignatura", "COD123", 6, "Carrera", 2, Departamento.DIIC)
    universidad.matricular("COD123", "123")
    universidad.desmatricular("COD123", "123")
    estudiante = universidad.devolverEstudiante("123")
    assert len(estudiante.asignaturas()) == 0

def test_vincular_profesor_asignatura():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_profesor("Jorge Larrey", "Calle Olmo", "54328-B", "a-4356", Sexo.Masculino, TipoMiembro.Asociado, Departamento.DIIC)
    universidad.incorporar_asignatura("Nombre Asignatura", "COD123", 6, "Carrera", 2, Departamento.DIIC)
    universidad.vincularProfesorAsignatura("COD123", "a-4356")
    profesor = universidad.devolverMiembro("a-4356")
    assert len(profesor.asignaturas()) == 1

def test_desvincular_profesor_asignatura():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_profesor("Jorge Larrey", "Calle Olmo", "54328-B", "a-4356", Sexo.Masculino, TipoMiembro.Asociado, Departamento.DIIC)
    universidad.incorporar_asignatura("Nombre Asignatura", "COD123", 6, "Carrera", 2, Departamento.DIIC)
    universidad.vincularProfesorAsignatura("COD123", "a-4356")
    universidad.desvincularProfesorAsignatura("COD123", "a-4356")
    profesor = universidad.devolverMiembro("a-4356")
    assert len(profesor.asignaturas()) == 0


def test_cambiar_identificador():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_profesor("Jorge Larrey", "Calle Olmo", "54328-B", "a-4356", Sexo.Masculino, TipoMiembro.Asociado, Departamento.DIIC)
    universidad.cambiarIdentificador("a-4356", "nuevo-identificador")
    profesor = universidad.devolverMiembro("nuevo-identificador")
    assert profesor is not None


def test_cambiar_numero_expediente():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    sexo = Sexo.Masculino
    universidad.incorporar_estudiante("Nombre Estudiante", "Dirección Estudiante", "12345678A", "123", sexo)
    universidad.cambiarNumeroExpediente("123", "456")
    estudiante = universidad.devolverEstudiante("456")
    assert estudiante is not None

def test_cambiar_codigo_asignatura():
    universidad = Universidad("Nombre Universidad", "Dirección Universidad")
    universidad.incorporar_asignatura("Nombre Asignatura", "COD123", 6, "Carrera", 2, Departamento.DIIC)
    universidad.cambiarCodigoAsignatura("COD123", "COD456")
    asignatura = universidad.devolverAsignatura("COD456")
    assert asignatura is not None





if __name__ == "__main__":

    e1 = Estudiante('Juan', 'Aurora, 8', '54673', 'e-9987',Sexo.Masculino)
    print(e1)
    #print(e1.devolver_direccion())
        

    p1 = ProfesorTitular('juan', 'Alcala', '44594', 'a-8889',Sexo.Masculino, TipoMiembro.Titular, Departamento.DIS, AreaInvestigacion.Software)
    print(p1)

#Creamos la universidad y añadimos a los estudiantes
#Véase como el ultimo estudiante está repetido.

    try:

        u = Universidad('Umu', 'Espinardo 6')
        u.incorporar_estudiante('Maria','Murcia 4','567845','e-33245',Sexo.Femenino)
        u.incorporar_estudiante('Marta', 'Murcia 12', '56784', 'e-3324879', Sexo.Femenino)
        u.incorporar_estudiante('Juan', 'Calle 34', '5644846', 'e-3324880', Sexo.Masculino)
        u.incorporar_estudiante('Alicia', 'Avenida 56', '5644847', 'e-3324881', Sexo.Femenino)
        u.incorporar_estudiante('Pedro', 'Plaza 78', '5644848', 'e-3324882', Sexo.Masculino)
        u.incorporar_estudiante('Ana', 'Carrera 90', '5644849', 'e-3324883', Sexo.Femenino)
        u.incorporar_estudiante('Luis', 'Paseo 112', '5644850', 'e-3324884', Sexo.Masculino)
        #u.incorporar_estudiante('Luis', 'Paseo 112', '5644850', 'e-3324884', Sexo.Masculino)

    except ExistingInformationError as msg:
        print(msg)
        
    except NotValidType as msg1:
        print(msg1)

    except IdentifierError as msg2:
        print(msg2)
        


#Añadimos a los profesores, e investigadores.
#Véase como el último profesor añadido (comenario), presenta el mismo código identificador que el profesor añadido justo antes, de forma que saltará la excepción.
#Véase como el último investigador añadido (comenario), es repetido, por lo que presenta un dni ya incorporado al sistema, lo que hace que salte la excepción.

    try:

        u.incorporar_profesor('Jorge Larrey', 'Calle Olmo', '54328-B', 'a-4356',Sexo.Masculino, TipoMiembro.Asociado, Departamento.DIIC)
        u.incorporar_profesor('Ana Martínez', 'Calle del Bosque', '54321-A', 'a-9876', Sexo.Femenino, TipoMiembro.Titular, Departamento.DIIC, AreaInvestigacion.Software)
        u.incorporar_profesor('Pedro Sánchez', 'Avenida del Rio', '98765-B', 'b-5432', Sexo.Masculino, TipoMiembro.Asociado, Departamento.DIS)
        u.incorporar_profesor('Laura Fernández', 'Calle de la Luna', '13579-C', 'c-2468', Sexo.Femenino, TipoMiembro.Titular, Departamento.DITEC, AreaInvestigacion.AprendizajeProfundo)
        u.incorporar_profesor('Luis Rodríguez', 'Carrera del Sol', '24680-D', 'd-1357', Sexo.Masculino, TipoMiembro.Asociado, Departamento.DIIC)
        u.incorporar_profesor('María García', 'Avenida de las Flores', '98765-E', 'e-8642', Sexo.Femenino, TipoMiembro.Titular, Departamento.DIIC, AreaInvestigacion.ComputacionAltasPrestaciones)
        u.incorporar_profesor('Juan Pérez', 'Calle de los Pinos', '54321-F', 'f-7293', Sexo.Masculino, TipoMiembro.Asociado, Departamento.DITEC)
        u.incorporar_profesor('Sofía Martín', 'Avenida de las Palmeras', '13579-G', 'g-5312', Sexo.Femenino, TipoMiembro.Titular, Departamento.DIS, AreaInvestigacion.InvestigacionOperativa)
        #u.incorporar_profesor('Martina Martinez', 'Avenida de las Palmeras', '13580-T', 'g-5312', Sexo.Femenino, TipoMiembro.Titular, Departamento.DIS, AreaInvestigacion.InvestigacionOperativa)

        u.incorporar_investigador('Manuel Molina', 'Plaza de la Libertad', '53453-A', 'i-9998653', Sexo.Masculino, Departamento.DITEC, AreaInvestigacion.ComputacionAltasPrestaciones )
        u.incorporar_investigador('Laura González', 'Calle del Sol', '54321-C', 'i-9876543', Sexo.Femenino, Departamento.DIIC, AreaInvestigacion.InvestigacionOperativa)
        u.incorporar_investigador('Carlos Martínez', 'Avenida de las Flores', '98765-D', 'i-1234567', Sexo.Masculino, Departamento.DIS, AreaInvestigacion.Software)
        u.incorporar_investigador('Ana García', 'Calle de los Pinos', '13579-E', 'i-2468101', Sexo.Femenino, Departamento.DITEC, AreaInvestigacion.AprendizajeMaquina)
        u.incorporar_investigador('David Sánchez', 'Avenida de las Palmeras', '98765-F', 'i-987654', Sexo.Masculino, Departamento.DIIC, AreaInvestigacion.AprendizajeProfundo)
        u.incorporar_investigador('María Rodríguez', 'Calle de la Luna', '54321-G', 'i-123456', Sexo.Femenino, Departamento.DIS, AreaInvestigacion.ArquitecturaDeComputadores)
        u.incorporar_investigador('Juan Pérez', 'Calle del Bosque', '13579-H', 'i-246810', Sexo.Masculino, Departamento.DITEC, AreaInvestigacion.ComputacionAltasPrestaciones)
        u.incorporar_investigador('Sofía Martín', 'Avenida del Rio', '98765-I', 'i-9876545', Sexo.Femenino, Departamento.DIIC, AreaInvestigacion.InvestigacionOperativa)
        u.incorporar_investigador('Pedro López', 'Plaza de la Libertad', '54321-J', 'i-1234563', Sexo.Masculino, Departamento.DIS, AreaInvestigacion.Software)
        u.incorporar_investigador('Laura Ruiz', 'Calle de las Rosas', '13579-K', 'i-2468108', Sexo.Femenino, Departamento.DITEC, AreaInvestigacion.AprendizajeMaquina)
        u.incorporar_investigador('Antonio González', 'Avenida de los Olivos', '98765-L', 'i-9876546', Sexo.Masculino, Departamento.DIIC, AreaInvestigacion.AprendizajeProfundo)
        u.incorporar_investigador('María Martínez', 'Calle de las Palmeras', '54321-M', 'i-1234562', Sexo.Femenino, Departamento.DIS, AreaInvestigacion.ArquitecturaDeComputadores)
        #u.incorporar_investigador('María Martínez', 'Calle de las Palmeras', '54321-M', 'i-1234562', Sexo.Femenino, Departamento.DIS, AreaInvestigacion.ArquitecturaDeComputadores)

    except NotValidType as msg1:
        print(msg1)
        

    except DepartamentoError as msg3:
        print(msg3)
        

    except IdentifierError as msg4:
        print(msg4)
        
    
    except ExistingInformationError as msg5:
        print(msg5)
        



#Añadimos asignaturas al sistema.
#Véase que si la asignatura ya existe, salta la excepción ExistingInformationError
#Véase que si la asignatura se ascocia a un deparatamento que no existe, salta la excepción DepartamentoError
#Véase que si a la asignatura se le pasa como créditos un tipo de dato que no es un número, salta la excepción NotValidType

    try:

        u.incorporar_asignatura('Mecánica de Fluidos', '5000001', 6, 'Ing. Mecánica', 1, Departamento.DIIC)
        u.incorporar_asignatura('Termodinámica', '5000002', 9, 'Ing. Mecánica', 2, Departamento.DIIC)
        u.incorporar_asignatura('Electromagnetismo', '5000003', 6, 'Ing. Electrónica', 2,  Departamento.DIIC)
        u.incorporar_asignatura('Programación Avanzada', '5000004', 12, 'Ing. Informática', 3, Departamento.DITEC)
        u.incorporar_asignatura('Diseño de Circuitos', '5000005', 6, 'Ing. Electrónica', 3,  Departamento.DIIC)
        u.incorporar_asignatura('Algoritmos Genéticos', '5000006', 16, 'Ing. Informática', 3,  Departamento.DITEC)
        u.incorporar_asignatura('Diseño de Sistemas', '5000007', 6, 'Ing. de Sistemas', 3, Departamento.DIS)
        u.incorporar_asignatura('Análisis Estructural', '5000008', 6, 'Ing. Civil', 2,  Departamento.DIIC)
        u.incorporar_asignatura('Control de Procesos', '5000009', 24, 'Ing. Química', 3, Departamento.DIIC)
        u.incorporar_asignatura('Termodinámica', '5000010', 6, 'Ing. Mecánica', 2, Departamento.DIIC)
        u.incorporar_asignatura('Electromagnetismo', '5000011', 6, 'Ing. Electrónica', 2,  Departamento.DIIC)
        u.incorporar_asignatura('Programación Avanzada', '5000012', 6, 'Ing. Informática', 3,  Departamento.DITEC)
        u.incorporar_asignatura('Diseño de Circuitos', '5000013', 4.5, 'Ing. Electrónica', 1,  Departamento.DIIC)
        u.incorporar_asignatura('Algoritmos Genéticos', '5000014', 3, 'Ing. Informática', 3, Departamento.DITEC)
        u.incorporar_asignatura('Diseño de Sistemas', '5000015', 2.5, 'Ing. de Sistemas', 4, Departamento.DIS)
        u.incorporar_asignatura('Análisis Estructural', '5000016', 4, 'Ing. Civil', 2,  Departamento.DIIC)
        u.incorporar_asignatura('Control de Procesos', '5000017', 6, 'Ing. Química', 3, Departamento.DIIC)
        #u.incorporar_asignatura('Control de Procesos', '50000100', 6, 'Ing. Química', 4, Departamento.DIIC)
        #u.incorporar_asignatura('Control de ProcesosII', '500001001', 6, 'Ing. Química', 3, 'Departamento de Qúmica')
        #u.incorporar_asignatura('Control de ProcesosIII', '5000017', 'a', 'Ing. Química', 3, Departamento.DIIC)

    
    except ExistingInformationError as ex:
        print(ex)

    except NotValidType as nv:
        print(nv)

    except DepartamentoError as d:
        print(d)


#Al mostrar la información en principio no debe haber ningún error

        a = u.devolverMiembro('i-246810')
        print(a)
        u.mostrar_estudiantes()
        print("\n")
        u.mostrar_investigadores()
        print("\n")
        u.mostrar_profesores()
        print("\n")



#Al mostrar las asignaturas asociadas a un departamento, si el departamento indicado no existiese salta la excepción DepartamentoError

    try:
        u.mostrar_asignaturas_departamento(Departamento.DITEC)
        print("\n")
        u.mostrar_miembros_departamento(Departamento.DIS)
        print("\n")
        #u.mostrar_miembros_departamento('DepartamentoSecreto')
    

    except DepartamentoError as d:
        print(d)



#Eliminamos algunos estudiantes y miembros del sistema. El término miembros engloba tanto a Profesores, como Investigadores.
#Véase que si el identificador pasado no se encuentra en el sistema, se lanza una excepción IdentifierError. 
#Además hay que llevar precaución, ya que puede que queramos eliminar un individuo que ya haya sido eliminado previamente.

    try:


        #u.eliminar_estudiante('aaaa')
        u.eliminar_estudiante('e-3324879')
        #u.eliminar_estudiante('e-3324879')
        u.eliminar_estudiante('e-3324880')
        u.eliminar_estudiante('e-3324883')
        u.eliminar_estudiante('e-3324884')

        
        u.mostrar_estudiantes()


        print("\n")
        u.eliminar_miembro('i-246810')
        u.eliminar_miembro('i-9998653')
        u.eliminar_miembro('i-1234567')
        u.eliminar_miembro('i-9876543')
        u.eliminar_miembro('i-2468101')

        u.mostrar_investigadores()

        print("\n")

        u.eliminar_miembro('a-4356')
        u.eliminar_miembro('a-9876')
        #u.eliminar_miembro('a-9876')

        u.mostrar_profesores()

        u.eliminar_asignatura('5000002')
        u.eliminar_asignatura('5000002')
        print("\n")

    except IdentifierError as id:
        print(id)


    
#Ahora probamos a matricular a un alumno de varias asignaturas, y mostrar entonces el listado de asignaturas a las que está matriculado dicho alumno.
#Tras mostrar las asignaturas, se prodece a desmatricularlo de una de ellas y volver a mostrar la lista de asignaturas a las que está vinculado el alumno,
#para poder ver si esta lista varía. 


    try:

        u.mostrar_asignaturas_departamento(Departamento.DIIC)
        
        u.cambiarDepartamento('i-9876546',Departamento.DIS)
    #Matriculo a un alumno de varias asignaturas
        
        u.matricular('5000001', 'e-3324881')
        u.matricular('5000004', 'e-3324881')
        u.matricular('5000005', 'e-3324881')
        u.matricular('5000006', 'e-3324881')

    #Muestro sus asignaturas
        alumno = u.devolverEstudiante('e-3324881')
        print("\n")
        alumno.mostrar_asignaturas()
    #Elimino la asignatura a la que primero lo matriculé
        print("\n")
        u.eliminar_asignatura('5000001')
        alumno.mostrar_asignaturas()
    #Lo desmatriculo de una de las asignaturas
        print("\n")
        u.desmatricular('5000004','e-3324881')
        alumno.mostrar_asignaturas()
    

    except IdentifierError as id:
        print(id)
    except DepartamentoError as d:
        print(d)


    print("\n")




#Vinculamos a un profesor cualquiera con algunas asignaturas, y mostramos las asignaturas de ese profesor, para posteriormente eliminar una asignatura a la que el profesor
#estaba vinculado, para ver si la asignatura desaparece de la lista de asinaturas del profesor.

    try:
    #Añado asignaturas a un profesor:
        u.vincularProfesorAsignatura('5000005','e-8642')
        u.vincularProfesorAsignatura('5000006','e-8642')
        u.vincularProfesorAsignatura('5000007','e-8642')

        profesor = u.devolverMiembro('e-8642')
        
        profesor.mostrar_asignaturas()

        print("\n")
        u.eliminar_asignatura('5000007')

        profesor.mostrar_asignaturas() 
        print("\n")

        print("Precio matrícula del alumno e-3324881:")
        u.calcularMatricula('e-3324881')
        print("\n")

    #Cambiamos el código de una asignatura, e intentamos mostrarla con su antiguo códifo y con el actual
        u.cambiarCodigoAsignatura('5000005', '1')
        print(u.devolverAsignatura('5000005'))
        print(u.devolverAsignatura('1'))

        print("\n")
    #Cambiamos el identificador de un miembro, e intentamos mostrarlo con su identificador antiguo y con el actual
        u.cambiarIdentificador( 'b-5432','2')
        print(u.devolverMiembro( 'b-5432'))
        print(u.devolverMiembro( '2'))


    except NotValidType as msg1:
        print(msg1)
    except DepartamentoError as msg2:
        print(msg2)
    except ExistingInformationError as msg3:
        print(msg3)
    except NotValidType as msg4:
        print(msg4)
    except IdentifierError as msg5:
        print(msg5)
     
        