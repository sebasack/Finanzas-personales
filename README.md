# finanzas-personales

operaciones:

    Ingresos:
        acreditacion sueldo
        sueldo efectivo
        sueldo efectivo negro
        Alquiler casa tio
        SUAF/anses
        cuenta DNI
        inversiones
        venta dolares
        varios
    impuestos
        arba
        inmobiliario
        patente
    servicios
        edes
        camuzzi
        seguro AUTOS
        seguro casa
        recarga celular
        gimnacio
        futbol
    supermercados
        cooperativa
        chango mas
        vea
        franco
        coto
    alimentacion
        verduleria
        carniceria
        polleria
        fabrica pastas
        panaderia
        dietetica
        quesos
        vinos
        pescaderia
        rotiseria
        heladeria
    educacion
        escuela
        ingles
        fotocopias
        utiles
    otros
        kiosco
        mercado libre
        regalos
        ropa
        peluqueria
        conciliacion
        ferreteria
        rifas
        varios
        recarga SUBE
        pago tarjeta credito
    esparcimiento
        salidas
        viajes
    gastos medicos
        farmacia
        visita medico
        analisis
        estudios
        bonos obra social
    auto
        nafta
        service
    indi
        veterinario
        comida
    inversiones
        bullmarket
        brubank
        fci
        plazo fijo
        ganancias
        perdidas
    transferencia
        entre cuentas
        a terceros

importe -> MEDIO DE PAGO |-> efectivo  
 |-> cuenta DNI  
 |-> bapro  
 |-> mercado pago  
 |-> tarjeta -> cuotas

tablas:
operaciones:
id
id_persona
id_tipo_operacion
fecha
monto
id_medio_pago
cuota (0=inmediato,1..n = nro de cuota)

        1;1;1;01/05/24;1520055;1;0          acreditacion sueldo
        2;1;2;02/05/24;605454;0;0           pago sueldo efectivo
        3;1;5;05/08/24;6689;5;1             pago arba con visa
        4;2;7;07/09/24;54654;3;0            pago super con mercado pago seba
        5;2;8;07/06/24;1100;5;1             pago vea visa cuota 1
        6;2;8;07/07/24;1100;5;2             pago vea visa cuota 2
        7;2;8;07/08/24;1100;5;3             pago vea visa cuota 3


tipos_operaciones:
id
descripcion  
 id_categoria
ids_medios_pago (1 o mas)

        1;0;Acreditacion sueldo;1;[2]
        2;0;Sueldo efectivo;1;[0]
        3;0;Alquiler tio;1;[4]
        4;1;Municipal;2;
        5;1;ARBA;2;[1,2,3,5]
        6;1;Carniceria;4;[0,1,2,3,4,5]
        7;1;Franco;4;[0,1,2,3,4,5]
        8;1;VEA;4;[0,1,2,3,4,5]

categorias:
id  
 descripcion  
 tipo (0=entrada,1=salida, 2=ambas)

        1;ingresos;0
        2;impuestos;1
        3;servicios;1
        4;Supermercado;1
        5;educacion;1
        6;otros;1
        7;inversiones;2
        8;transferencias;2

medios_pago:
id
tipo (0=efectivo,1=debito,2=credito)
ids_personas (1 o mas titulares)
descripcion
monto_disponible
dia_cierre
dia_pago

        1;0;[1,2,3,4];efectivo;6464,44;;
        2;1;[1,2];BAPRO;98798,33;;
        3;1;[1];MERCADO PAGO SEBA;9598,33;;
        4;1;[2];MERCADO PAGO FER;958,33;;
        5;2;[1,2];VISA SEBA;1500000;29;12

personas:
id
nombre

        1;sebastian
        2;fernanda
        3;ramiro
        4;tomas

---

PANTALLAS:

    principal
     ___________________
    | Nueva transaccion |
    |      Saldos       |
    |  Configuraciones  |
    |       Salir       |
    |___________________|

            Nueva transaccion
             ___________________
            |  importe: 1200.00 |
            |      Cancelar     |
            |___________________|

                    Ingresar categoria (ordenadas de mas usado a menos usado por la persona)
                     ___________________
                    |     Impuestos     |
                    |    supermercado   |
                    |     educacion     |
                    |       otros       |
                    |        ...        |
                    |       Volver      |
                    |      Cancelar     |
                    |___________________|

                            Ingresar operacion  (ordenadas de mas usado a menos usado por la persona)
                             ___________________
                            |    Cooperativa    |
                            |       Franco      |
                            |     Chango mas    |
                            |        VEA        |
                            |        ...        |
                            |   Nueva operacion |
                            |       Volver      |
                            |      Cancelar     |
                            |___________________|


                                    ingresar medio de pago (muestra los medios de pago asociados a la persona, ordenados po uso)
                                     ___________________
                                    |      Efectivo     |
                                    |       BAPRO       |
                                    |         MP        |
                                    |        ...        |
                                    |       Volver      |
                                    |      Cancelar     |
                                    |___________________|

                                            ingresar fecha
                                             ___________________
                                            |      GUARDAR      |
                                            | Fecha: 10/05/2024 |
                                            |       Volver      |
                                            |      Cancelar     |
                                            |___________________|

            configuraciones
             ___________________
            | Tipos operaciones |
            |    Categorias     |
            |  Medios de pago   |
            |      Personas     |
            |      Volver       |
            |___________________|

                    tipos operaciones
                     ___________________
                    |    Nuevo tipo     |
                    |  Modificiar tipo  |
                    |   Eliminar tipo   |
                    |      Volver       |
                    |     Cancelar      |
                    |___________________|

                            Nuevo tipo:
                                1 elige descripcion
                                2 elige categoria
                                3 elige medios de pago

                    categorias
                     ___________________
                    |  Nueva categoria  |
                    |  Modificiar cat.  |
                    | Eliminar categoria|
                    |       Volver      |
                    |      Cancelar     |
                    |___________________|

                            Nueva categoria:
                                1 elige descripcion
                                2 elige tipo (entrada o salida)


                    Medios de pago
                     ___________________
                    |    Nuevo Medio    |
                    | Modificiar Medio  |
                    |  Eliminar Medio   |
                    |       Volver      |
                    |      Cancelar     |
                    |___________________|

                            nuevo medio de pago:
                                1 carga descripcion
                                2 elige tipo (0=efectivo,1=debito,2=credito)
                                3 elije personas (1 o mas)
                                4 monto_disponible (si es credito)
                                5 dia_cierre       (si es credito)
                                6 dia_pago         (si es credito)



                    personas
                     ___________________
                    |   Nueva persona   |
                    | Eliminar persona  |
                    |       Volver      |
                    |      Cancelar     |
                    |___________________|

                            nueva persona
                                1 elige nombre


     Saldos
             ___________________________
            | Efectivo:         6464,22 |
            | BAPRO:           64646,58 |
            | MERCADO PAGO SEBA 9598,33 |
            | MERCADO PAGO fer  4535,33 |
            |                  74548,64 |
            |___________________________|
            | VISA (12/08)    -90234,23 |
            |___________________________|
            | bullmarket        4535,33 |
            | fci                635,33 |
            |                   5548,64 |
            |___________________________|
            |    Exportar informacion   |
            |___________________________|


