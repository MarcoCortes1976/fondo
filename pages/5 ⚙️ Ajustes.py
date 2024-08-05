import streamlit as st
import pandas as pd
import json
import Funciones

st.set_page_config(layout="wide")

st.title('Ajustes')

control_1, control_2 = False, False

try:
    with open('ajustes.json', 'r') as j_a:
        j_a.close()

    control_1 = True
except:
    st.error('Se necesita un archivo de ajustes.', icon="🚨")

try:
    with open('ajustes.json', 'r') as j_a:
        ajustes = json.load(j_a)
        j_a.close()

    df = pd.read_csv(ajustes['nombre df'])

    control_2 = True
except:
    st.error('Se necesita una tabla de socios.', icon="🚨")

if not (control_1 and control_2):

    st.header('Creacion de archivos para control y almacenamiento.')

    c1_1, c1_2 = st.columns(2)

    with c1_1:
        if st.button('crear ajustes de el programa'):
            Funciones.crear_ajustes_de_el_programa()
            st.success('Los ajustes han sido configurados', icon="✅")

    with c1_2:
        if st.button('Crear nueva tabla de socios'):
            Funciones.crear_data_frame_principal()
            st.success('La tabla ha sido creada', icon="✅")

else:
    if st.session_state['preguntar clave']:
        clave = st.text_input('Por favor introduzca la contraseña.')

        if st.button('Continuar'):
            if clave == st.session_state.clave_de_acceso:
                st.session_state['preguntar clave'] = False
                st.rerun()
            elif clave == '':
                st.error('La contraseña esta vacia', icon="🚨")
            else:
                st.error('La contraseña no es correcta', icon="🚨")

    else:
        with open('ajustes.json', 'r') as f:
            ajustes = json.load(f)
            f.close()

        tab_1, tab_2, tab_3, tab_4, tab_5, tab_6, tab_7, tab_8 = st.tabs([
            'Calendario', 'Cuotas y multas', 'Contraseñas', 'Intereses', 'Usuarios',
            'Fechas', 'Tabla de socios', 'Guardar datos'
        ])

        with tab_1:
            st.header('Calendario')

            calendario = ajustes['calendario']

            if calendario == '-':
                st.error('No hay un calendario.', icon="🚨")
            else:
                calendario = calendario.split('-')
                hora_de_corte = calendario[1][-2:]
                calendario = list(map(lambda x: x[:-3], calendario))
                #calendario += ['____/__/__']

                st.write(f'Hora de corte: {hora_de_corte}')
                st.table(pd.DataFrame({'columna 1': calendario[:10],
                                       'columna 2': calendario[10:20],
                                       'columna 3': calendario[20:30],
                                       'columna 4': calendario[30:40],
                                       'columna 5': calendario[40:]
                                       }))

            st.subheader('Crear calendario.')

            n_hora = st.number_input('Hora de corte.', value=0, step=1)

            n_fecha_inicial = st.date_input('Fecha inicial.')
            n_fecha_doble_1 = st.date_input('Primera fecha doble.')
            n_fecha_doble_2 = st.date_input('Segunda fecha doble.')

            if st.button('Crear calendario'):
                n_fecha_inicial = n_fecha_inicial.strftime('%Y/%m/%d') + '/' + str(n_hora)
                n_fecha_doble_1 = n_fecha_doble_1.strftime('%Y/%m/%d') + '/' + str(n_hora)
                n_fecha_doble_2 = n_fecha_doble_2.strftime('%Y/%m/%d') + '/' + str(n_hora)

                if n_fecha_doble_1 == n_fecha_doble_2:
                    st.error('Las fechas dobles no pueden coincidir', icon="🚨")
                else:
                    n_dobles = [n_fecha_doble_1, n_fecha_doble_2]

                    fechas = Funciones.crear_listado_de_fechas(
                        primera_fecha=n_fecha_inicial, dobles=n_dobles
                    )
                    s_fechas = '-'.join(fechas)
                    ajustes['calendario'] = s_fechas

                    with open('ajustes.json', 'w') as f:
                        json.dump(ajustes, f)
                        f.close()

                    st.rerun()

        with tab_2:

            st.header('Valor de la cuota por puesto y por multa.')

            st.info(
                'Por favor al ingresar cantidades en miles no ingrese las comas, solo el numero plano.',
                icon="ℹ️"
            )

            st.subheader('Por puesto.')
            st.write(f'Valor de la cuota por puesto: {'{:,}'.format(ajustes['valor cuota'])}')
            n_cuota_puesto = st.number_input('Nuevo valor de la cuota.', value=0, step=1)

            if st.button('Modificar.', key='00001'):
                ajustes['valor cuota'] = n_cuota_puesto
                st.session_state.valor_de_la_cuota = n_cuota_puesto

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado. ', icon="✅")
                st.rerun()

            st.subheader('Por multa.')
            st.write(f'Valor de la multa por puesto: {'{:,}'.format(ajustes['valor multa'])}')
            n_cuota_multa = st.number_input('Nuevo valor de la multa.', value=0, step=1)

            if st.button('Modificar', key='00002'):
                ajustes['valor multa'] = n_cuota_multa
                st.session_state.valor_de_la_multa = n_cuota_multa

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_3:

            st.header('Clave de acceso.')

            st.write(f'La clave actual es: {ajustes['clave de acceso']}')
            st.subheader('Modificar clave de acceso.')
            nueva_clave = st.text_input('Nueva clave de acceso.')

            if st.button('Modificar.', key='00003'):
                ajustes['clave de acceso'] = nueva_clave
                st.session_state.clave_de_acceso = nueva_clave

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_4:
            st.header('Tope de intereses.')

            st.write(
                f'Tope de diferencia entre intereses de prestamo: {
                '{:,}'.format(ajustes['tope de intereses'])
                }'
            )
            nuevo_tope = st.number_input('Nuevo tope de intereses.', value=0, step=1)

            if st.button('Modificar.', key='00013'):
                ajustes['tope de intereses'] = nuevo_tope
                st.session_state.tope = nuevo_tope

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.header('Interes por prestamo.')

            st.subheader('Menos de el tope.')
            st.write(f'el interes actual por prestamo es: {ajustes['interes < tope']}')
            st.subheader('Modificar el interes.')

            nuevo_interes_m_tope = st.number_input('Nuevo interes.', value=0, step=1, key='00010')

            if st.button('Modificar.', key='00004'):
                ajustes['interes < tope'] = nuevo_interes_m_tope
                st.session_state.interes_menos_20M = nuevo_interes_m_tope

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Mas de el tope.')

            st.write(f'el interes actual por prestamo es: {ajustes['interes > tope']}')
            st.subheader('Modificar el interes.')
            nuevo_interes_M_tope = st.number_input('Nuevo interes.', value=0, step=1, key='00009')

            if st.button('Modificar.', key='00008'):
                ajustes['interes > tope'] = nuevo_interes_M_tope
                st.session_state.interes_mas_20M = nuevo_interes_M_tope

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_5:
            st.header('Usuarios')

            st.subheader('Numero de usuarios')

            st.write(f'El numero actual de usuarios es el programa es: {ajustes['usuarios']}')
            nuevo_usuarios = st.number_input('Nuevo numero de usuarios.', value=0, step=1)

            if st.button('Modificar.', key='00005'):
                ajustes['usuarios'] = nuevo_usuarios
                st.session_state.usuarios = nuevo_usuarios

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Desactivar usuarios.')
            desactivar_usuarios = ajustes['anular usuarios']

            if desactivar_usuarios:
                st.write('Los usuarios seran desactivados.')
            else:
                st.write('Los usuarios NO seran desactivados.')

            if st.button('invertir', key='00006'):
                desactivar_usuarios = not desactivar_usuarios
                st.session_state.anular_usuarios = desactivar_usuarios
                ajustes['anular usuarios'] = desactivar_usuarios

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Cobrar multas.')
            cobra_multas = ajustes['cobrar multas']

            if cobra_multas:
                st.write('Actualmente se generan multas.')
            else:
                st.write('Actualmete NO se generan multas.')


            if st.button('invertir', key='00007'):
                cobra_multas = not cobra_multas
                st.session_state.cobrar_multas = cobra_multas
                ajustes['cobrar multas'] = cobra_multas

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_6:
            st.subheader(f'Fecha de cierre.')

            st.write(f'Fecha de cierre actual: {ajustes['fecha de cierre']}')
            n_fecha = st.date_input('Nueva fecha de cierre.')

            if st.button('Modificar', key='000014'):
                n_fecha = n_fecha.strftime('%Y/%m/%d')
                ajustes['fecha de cierre'] = n_fecha

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_7:
            st.subheader('Nombre de la tabla.')

            st.write(f'Tabla de trabajo actual: {ajustes['nombre df']}')
            n_nombre_tabla = st.text_input('Nuevo nombre.')

            if st.button('Modificar', key='00015'):
                ajustes['nombre df'] = n_nombre_tabla
                st.session_state.nombre_df = n_nombre_tabla

                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Numero de generacion.')

            st.write(f'Numero de generacion actual: {ajustes['numero de creacion']}')
            n_numero_gen = st.number_input('Nuevo numero de generacion.', value=0, step=1)

            if st.button('Modificar', key='00016'):
                ajustes['numero de creacion'] = n_numero_gen
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

        with tab_8:
            st.subheader('Ruta de el programa')

            st.write(f'Ruta de el programa: {ajustes['path programa']}')
            n_ruta = st.text_input('Nuevo token de conexion.')

            if st.button('Modificar', key='00017'):
                ajustes['path programa'] = n_ruta
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()

            st.subheader('Enlace de el repositorio')

            st.write(f'Enlace actual: {ajustes['enlace repo']}')
            n_tablas_g = st.text_input('Nuevo enlace.', value=0, step=1)

            if st.button('Modificar', key='00018'):
                ajustes['enlace repo'] = n_tablas_g
                with open('ajustes.json', 'w') as f:
                    json.dump(ajustes, f)
                    f.close()

                st.success('Valor modificado.', icon="✅")
                st.rerun()