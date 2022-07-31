import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode

TEMPLATE_DIRECTORY = '.'

df = pd.DataFrame(data=[['name1', 179, 'rand1', 1.77082580098645,
                         'Vl_1', 'Value1', 0.597755576753429,
                         0.565721911608865],
                        ['name2', 636, 'rand2', 0.0692480124621976,
                         'Vl_1', 'Value2',
                         1.61898499115126, 0.12230805081684],
                        ['name3', 609, 'rand3', 0.0548686377158919,
                         'Vl_2', 'Value1',
                         1.29469153390819, 0.179592362943293],
                        ['name4', 26, 'rand4', 0.287184715631094,
                         'Vl_1', 'Value2',
                         0.0705337998505417, 0.991618994618079],
                        ['name5', 672, 'rand5', 0.620180349089237,
                         'Vl_2', 'Value1',
                         0.812572721889621, 0.124504337847362]],
                  columns=['Name', 'Col1', 'Col2', 'Col3',
                           'Col4', 'Col5', 'Col6', 'Col7'])


def buildcoldefs(df):

    cols1 = ['Value1', 'Value2', 'Value3']
    cols2 = ['Vl_1', 'Vl_2', 'Vl_3']

    cols3 = list(df.Name.unique())

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column('Name',     editable=True, checkboxSelection=True)
    gb.configure_column('Col1', editable=True),
    gb.configure_column('Col2', editable=True, type=[
                        'numericColumn', 'numberColumnFilter',
                        'customNumericFormat'], precision=3, groupable=False)
    gb.configure_column('Col3', editable=True, type=[
                        'numericColumn', 'numberColumnFilter',
                        'customNumericFormat'], precision=2)
    gb.configure_column('Col4', editable=True, type=[
                        'numericColumn', 'numberColumnFilter',
                        'customNumericFormat'], precision=2)
    gb.configure_column('Col5', editable=True,
                        cellEditor='agSelectCellEditor',
                        cellEditorParams={'values': cols3})
    gb.configure_column('Col6', editable=True, cellEditor='agSelectCellEditor',
                        cellEditorParams={'values': cols1}, groupable=True)
    gb.configure_column('Col7', editable=True,
                        cellEditor='agSelectCellEditor',
                        cellEditorParams={'values': cols2})
    gb.configure_column('Col8',   editable=True),
    gb.configure_auto_height(True)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=8)

    groupSelectsChildren = False
    groupSelectsFiltered = False
    selection_mode = 'multiple'
    gb.configure_selection(selection_mode, use_checkbox=True,
                           suppressRowClickSelection=True,
                           groupSelectsChildren=groupSelectsChildren,
                           groupSelectsFiltered=groupSelectsFiltered)

    gbdef = gb.build()
    return(gbdef)


def get_definitions_page(df):
    slider = st.selectbox('Choose a Template', options=[
                          'opt1', 'opt2', 'opt3'])
    if 'df' not in st.session_state:
        st.session_state['df'] = df

    gbdef = buildcoldefs(df)

    st.subheader("Definitions")


    grid = AgGrid(st.session_state.df, gridOptions=gbdef,
                                    editable=True,
                                    fit_columns_on_grid_load=True,
                                    enable_enterprise_modules=True,
                                    update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED
                  |GridUpdateMode.MANUAL,
                                    reload_data=True,
                                    allow_unsafe_jscode=True)


    st.session_state.selected = grid['selected_rows']
    dfcompare = grid['data'].compare(st.session_state.df)
    if grid['event'] is not None:
        df = grid.get('data')
        event = grid['event']
        if event['type'] == 'ContextMenuClicked':
            row = event['row']
            if event['name'] == 'Delete row':
                index = df.index[row]
                st.write(index)
                df = df.drop(index, inplace=True)
                #df = df.drop(index)
                st.session_state.df = df
                st.write(df)
            if event['name'] == 'Insert row':
                df_before = df.iloc[:row]
                df_after = df.iloc[row:]
                df_new = pd.DataFrame([[None] * len(df.columns)],
                                    columns=df.columns)
                df = pd.concat((df_before, df_new, df_after))
                st.session_state.df = df
                st.write(df)
            st.experimental_rerun()
        st.write(event)
    if not dfcompare.empty:         # check if it changed
        st.session_state.df = grid['data']
    return()


if __name__ == "__main__":
    get_definitions_page(df)
