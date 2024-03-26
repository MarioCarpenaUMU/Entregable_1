from abc import ABCMeta, abstractmethod
from enum import Enum
import pytest
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
def estudiante_ejemplo():
    return Estudiante('Juan', 'Aurora, 8', '54673', 'e-9987', Sexo.Masculino)


def profesor_titular_ejemplo():
    return ProfesorTitular('Juan', 'Alcala', '44594', 'a-8889', Sexo.Masculino, TipoMiembro.Titular, Departamento.DIS, AreaInvestigacion.Software)


def profesor_asociado_ejemplo():
    return ProfesorAsociado('Maria', 'Madrid', '44678', 'a-6678', Sexo.Femenino, TipoMiembro.Asociado, Departamento.DIIC)


def investigador_ejemplo():
    return Investigador('Pedro', 'Gran Via, 25', '98765', 'i-6789', Sexo.Masculino, TipoMiembro.Investigador, Departamento.DIS, AreaInvestigacion.InvestigacionOperativa)

def test_estudiante():
    estudiante = estudiante_ejemplo()
    assert estudiante.nombre == 'Juan'
    assert estudiante.numero_expediente == 'e-9987'

def test_profesor_titular():
    profesor_titular = profesor_titular_ejemplo()
    assert profesor_titular.nombre == 'Juan'
    assert profesor_titular.area_investigacion == AreaInvestigacion.Software

def test_profesor_asociado():
    profesor_asociado = profesor_asociado_ejemplo()
    assert profesor_asociado.nombre == 'Maria'
    assert profesor_asociado.tipo == TipoMiembro.Asociado

def test_investigador():
    investigador = investigador_ejemplo()
    assert investigador.nombre == 'Pedro'
    assert investigador.area_investigacion == AreaInvestigacion.InvestigacionOperativa

if __name__ == "__main__":
    ## Podemos ver los resultados:
    e1 = Estudiante('Juan', 'Aurora, 8', '54673', 'e-9987',Sexo.Masculino)

    p_a_1=ProfesorAsociado('Maria', 'Madrid', '44678', 'a-6678', Sexo.Femenino, TipoMiembro.Asociado, Departamento.DIIC)
    p1 = ProfesorTitular('Juan', 'Alcala', '44594', 'a-8889',Sexo.Masculino, TipoMiembro.Titular, Departamento.DIS, AreaInvestigacion.Software)
    i1 = Investigador('Pedro', 'Gran Via, 25', '98765', 'i-6789', Sexo.Masculino, TipoMiembro.Investigador, Departamento.DIS, AreaInvestigacion.InvestigacionOperativa)
    print(e1)
    print(p_a_1)
    print(p1)
    print(i1)


        