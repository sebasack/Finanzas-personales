# finanzas-personales

opciones de otro bot:

-   /open - iniciar la aplicación;
-   Estadísticas o /stats - muestra tus gastos;
-   Eliminar o /delete - eliminar tu último registro;
-   Historial o /list - obtienes la lista de todos los registros;
-   Exportar o /export - descargas el historial en formato CSV;
-   Cancelar o /cancel - cancelar la operación actual;
-   Ajustes o /settings - configuración del bot;
-   Establecer moneda o /set_currency - establecer la moneda principal;
-   Establecer idioma o /set_lang - cambiar el idioma;
-   Suscripción o /subscription - obtenga información sobre las funcionalidades de pago;
-   Ayuda o /help - obtén esta información de ayuda.
-   Listar categorías o /list_categories
-   Añadir categoría o /add_category
-   Editar categoría o /edit_category
-   Eliminar categoría o /delete_category

---

operaciones:

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
    mascotas:
        veterinario
        comida
    inversiones:
        bullmarket
        brubank
        fci
        plazo fijo
        ganancias
        perdidas
    transferencia:
        entre cuentas
        a terceros

    Ingresos:
        acreditacion sueldo
        sueldo efectivo
        sueldo efectivo 2
        Alquileres
        SUAF/anses
        Promociones
        inversiones
        venta dolares
        varios
    impuestos:
        arba
        inmobiliario
        patente
    servicios:
        edes
        camuzzi
        seguro auto
        seguro casa
        recarga celular
        gimnacio
        futbol

importe -> Categoria -> Subcategoria -> MEDIO DE PAGO |-> efectivo  
 |-> cuenta DNI  
 |-> bapro  
 |-> mercado pago  
 |-> tarjeta -> cuotas

PANTALLAS:

    ingresa un numero:

        1200.00

            Ingresar categoria (ordenadas de mas usado a menos usado por el usuario)
             ___________________
            |     Impuestos     |
            |    supermercado   |
            |     educacion     |
            |       otros       |
            |        ...        |
            |      Cancelar     |
            |___________________|

                    Ingresar subcategoria  (ordenadas de mas usado a menos usado por el usuario)
                     ___________________
                    |    Cooperativa    |
                    |       Franco      |
                    |     Chango mas    |
                    |        VEA        |
                    |        ...        |
                    |   Nueva operacion |
                    | Cambiar categoria |
                    |      Cancelar     |
                    |___________________|


                            ingresar medio de pago (muestra los medios de pago asociados a la subcategoria y al usuario, ordenados por uso)
                             _____________________
                            |       Efectivo      |
                            |        BAPRO        |
                            |          MP         |
                            |         ...         |
                            | Cambiar subcategoria|
                            |       Cancelar      |
                            |_____________________|

                                    ingresar datos extras
                                     ___________________
                                    |      GUARDAR      |
                                    |   Cambiar Fecha   |
                                    |       Volver      |
                                    |      Cancelar     |
                                    |___________________|


    Opciones
     ___________________
    |      Saldos       |
    |   operaciones     |
    |  Configuraciones  |
    |       Salir       |
    |___________________|

            configuraciones
             ___________________
            |    Categorias     |
            |   subcategorias   |
            |  Medios de pago   |
            |     usuarios      |
            |      Salir        |
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



                    usuarios
                     ___________________
                    |   Nuevo usuario   |
                    | Eliminar usuario  |
                    |       Volver      |
                    |      Cancelar     |
                    |___________________|

                            nueva usuario
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


    operaciones:
