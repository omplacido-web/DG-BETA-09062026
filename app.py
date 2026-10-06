# ============================================================
# app.py
# ============================================================
# Data Governance Control Center
#
# VISUAL DESIGN
# ------------------------------------------------------------
# Royal Blue = Primary / Sidebar / Branding
# Teal      = Content boxes / Sections / Actions
# Gold      = Small accent
# White     = Input fields
# Dark Text = Text inside white input fields
#
# NO BLACK INPUT BOXES
# NO BLACK HIGHLIGHTS
# ============================================================

import streamlit as st
import pandas as pd
from datetime import datetime

from owner_registry import (
    save_owner_registry,
    get_cde_registry,
    import_owner_registry_from_csv,
    save_ownership_assignment,
    get_complete_owner_registry,
    delete_owner_registry,
    save_cde,
    update_cde,
    delete_cde,
    save_cde_assessment
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Data Governance Control Center",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# COLOR PALETTE
# ============================================================

PRIMARY = "#293296"
SECONDARY = "#359FB6"
TERTIARY = "#F2B949"

WHITE = "#FFFFFF"
LIGHT_BACKGROUND = "#F4F8FA"
DARK_TEXT = "#3F4A5A"
LIGHT_BORDER = "#D9DEE7"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ========================================================
       MAIN APPLICATION
       ======================================================== */

    .stApp {{
        background-color: {LIGHT_BACKGROUND};
    }}


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {{
        background-color: {PRIMARY} !important;
        border-right: 0 !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: {WHITE} !important;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {WHITE} !important;
    }}

    section[data-testid="stSidebar"] p {{
        color: {WHITE} !important;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        color: {WHITE} !important;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background-color: {SECONDARY} !important;
        border-radius: 6px;
    }}


    /* ========================================================
       MAIN TITLES
       ======================================================== */

    h1 {{
        color: {PRIMARY} !important;
        font-weight: 700 !important;
    }}

    h2 {{
        color: {PRIMARY} !important;
        font-weight: 700 !important;
    }}

    h3 {{
        color: {PRIMARY} !important;
        font-weight: 700 !important;
    }}

    h4,
    h5,
    h6 {{
        color: {PRIMARY} !important;
    }}


    /* ========================================================
       NORMAL PAGE TEXT
       ======================================================== */

    .stApp p {{
        color: {DARK_TEXT};
    }}


    /* ========================================================
       TEAL CONTENT BOXES
       ======================================================== */

    div[data-testid="stExpander"] {{
        background-color: {SECONDARY} !important;
        border: 0 !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
    }}

    div[data-testid="stExpander"] summary {{
        background-color: {SECONDARY} !important;
        border-radius: 8px !important;
    }}

    div[data-testid="stExpander"] summary span {{
        color: {WHITE} !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stExpander"] > details > div {{
        background-color: {SECONDARY} !important;
    }}

    div[data-testid="stExpander"] label {{
        color: {WHITE} !important;
    }}


    /* ========================================================
       INPUT BOXES
       ======================================================== */

    input {{
        background-color: {WHITE} !important;
        color: {DARK_TEXT} !important;
        border: 1px solid {LIGHT_BORDER} !important;
        border-radius: 6px !important;
    }}

    textarea {{
        background-color: {WHITE} !important;
        color: {DARK_TEXT} !important;
        border: 1px solid {LIGHT_BORDER} !important;
        border-radius: 6px !important;
    }}

    input:focus,
    textarea:focus {{
        background-color: {WHITE} !important;
        color: {DARK_TEXT} !important;
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 1px {PRIMARY} !important;
    }}


    /* ========================================================
       SELECT BOXES
       ======================================================== */

    div[data-baseweb="select"] > div {{
        background-color: {WHITE} !important;
        color: {DARK_TEXT} !important;
        border: 1px solid {LIGHT_BORDER} !important;
        border-radius: 6px !important;
    }}

    div[data-baseweb="select"] span {{
        color: {DARK_TEXT} !important;
    }}


    /* ========================================================
       NUMBER INPUTS
       ======================================================== */

    div[data-testid="stNumberInput"] input {{
        background-color: {WHITE} !important;
        color: {DARK_TEXT} !important;
        border: 1px solid {LIGHT_BORDER} !important;
    }}


    /* ========================================================
       ACTION BUTTONS
       ======================================================== */

    div.stButton > button {{
        background-color: {SECONDARY} !important;
        color: {WHITE} !important;
        border: 1px solid {SECONDARY} !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
    }}

    div.stButton > button:hover {{
        background-color: {PRIMARY} !important;
        color: {WHITE} !important;
        border-color: {PRIMARY} !important;
    }}


    /* ========================================================
       DOWNLOAD BUTTONS
       ======================================================== */

    div.stDownloadButton > button {{
        background-color: {SECONDARY} !important;
        color: {WHITE} !important;
        border: 1px solid {SECONDARY} !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
    }}

    div.stDownloadButton > button:hover {{
        background-color: {PRIMARY} !important;
        color: {WHITE} !important;
        border-color: {PRIMARY} !important;
    }}


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    section[data-testid="stFileUploaderDropzone"] {{
        background-color: {WHITE} !important;
        border: 2px dashed {SECONDARY} !important;
        border-radius: 8px !important;
    }}

    section[data-testid="stFileUploaderDropzone"] * {{
        color: {DARK_TEXT} !important;
    }}


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {{
        border: 2px solid {SECONDARY} !important;
        border-radius: 8px !important;
    }}


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {{
        background-color: {SECONDARY} !important;
        border-radius: 8px !important;
        padding: 18px !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {WHITE} !important;
    }}

    div[data-testid="stMetricLabel"] p {{
        color: {WHITE} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {WHITE} !important;
    }}


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {{
        border-radius: 6px !important;
    }}


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {{
        border-color: {SECONDARY} !important;
        opacity: 0.35;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛡️ Data Governance")
st.sidebar.caption("Control Center")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Data Owner Registry",
        "Data Catalog",
        "Classification Engine",
        "CDE Identification Tool",
        "CDE Engine",
        "Policies & Standards"
    ]
)


# ============================================================
# REGISTRY DISPLAY LABELS
# ============================================================

REGISTRY_LABELS = {

    "entity_id": "Entity ID",

    "entity_name": "Entity Name",

    "description": "Description",

    "data_domain": "Data Domain",

    "data_classification": "Data Classification",

    "ownership_assignment_id":
        "Ownership Assignment ID",

    "ownership_scope":
        "Ownership Scope",

    "program":
        "Program",

    "data_owner_division_head":
        "Data Owner - Division Head",

    "data_owner_division":
        "Data Owner Division",

    "data_owner_department_head":
        "Data Owner - Department Head",

    "data_owner_department":
        "Data Owner Department",

    "data_steward_1_division_head":
        "Data Steward 1 - Division Head",

    "data_steward_1_division":
        "Data Steward 1 Division",

    "data_steward_1_department_head":
        "Data Steward 1 - Department Head",

    "data_steward_1_department":
        "Data Steward 1 Department",

    "data_steward_2_division_head":
        "Data Steward 2 - Division Head",

    "data_steward_2_division":
        "Data Steward 2 Division",

    "data_steward_2_department_head":
        "Data Steward 2 - Department Head",

    "data_steward_2_department":
        "Data Steward 2 Department",

    "data_steward_3_division_head":
        "Data Steward 3 - Division Head",

    "data_steward_3_division":
        "Data Steward 3 Division",

    "data_steward_3_department_head":
        "Data Steward 3 - Department Head",

    "data_steward_3_department":
        "Data Steward 3 Department",

    "data_custodian_1_division_head":
        "Data Custodian 1 - Division Head",

    "data_custodian_1_division":
        "Data Custodian 1 Division",

    "data_custodian_1_department_head":
        "Data Custodian 1 - Department Head",

    "data_custodian_1_department":
        "Data Custodian 1 Department",

    "data_custodian_2_division_head":
        "Data Custodian 2 - Division Head",

    "data_custodian_2_division":
        "Data Custodian 2 Division",

    "data_custodian_2_department_head":
        "Data Custodian 2 - Department Head",

    "data_custodian_2_department":
        "Data Custodian 2 Department",

    "data_custodian_3_division_head":
        "Data Custodian 3 - Division Head",

    "data_custodian_3_division":
        "Data Custodian 3 Division",

    "data_custodian_3_department_head":
        "Data Custodian 3 - Department Head",

    "data_custodian_3_department":
        "Data Custodian 3 Department"
}


def prepare_registry_for_display(dataframe):

    dataframe = dataframe.copy()

    dataframe = dataframe.rename(
        columns={
            column: REGISTRY_LABELS[column]
            for column in dataframe.columns
            if column in REGISTRY_LABELS
        }
    )

    return dataframe


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("Data Governance Control Center")

    st.write(
        "Centralized management of data governance controls, "
        "ownership, classification, critical data elements "
        "and policies."
    )

    st.divider()

    registry = get_complete_owner_registry()

    cde_registry = get_cde_registry()

    entity_count = 0
    ownership_count = 0

    if not registry.empty:

        entity_count = registry["entity_id"].nunique()
        ownership_count = len(registry)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Data Entities",
            entity_count
        )

    with col2:

        st.metric(
            "Ownership Assignments",
            ownership_count
        )

    with col3:

        st.metric(
            "CDE Records",
            len(cde_registry)
        )


# ============================================================
# DATA OWNER REGISTRY
# ============================================================

elif page == "Data Owner Registry":

    st.title("Data Owner Registry")

    st.write(
        "Manage Data Entities, Ownership Assignments, "
        "Data Stewards and Data Custodians."
    )

    st.divider()


    # ========================================================
    # COMPLETE REGISTRY
    # ========================================================

    st.subheader("Complete Data Owner Registry")

    registry = get_complete_owner_registry()

    if registry.empty:

        st.info(
            "No Data Owner Registry records found."
        )

    else:

        display_registry = prepare_registry_for_display(
            registry
        )

        search_text = st.text_input(
            "Search Registry",
            placeholder=(
                "Search Entity ID, Entity Name, Data Domain, "
                "Ownership Scope, Program, Data Owner..."
            )
        )

        if search_text:

            search_text = search_text.lower()

            matching_rows = display_registry.apply(
                lambda row:
                    row.astype(str)
                    .str.lower()
                    .str.contains(
                        search_text,
                        na=False
                    )
                    .any(),
                axis=1
            )

            display_registry = display_registry[
                matching_rows
            ]

        st.dataframe(
            display_registry,
            use_container_width=True,
            hide_index=True
        )


    st.divider()


    # ========================================================
    # DELETE DATA ENTITY
    # ========================================================

    st.subheader("Delete Data Entity")

    delete_registry = get_complete_owner_registry()

    if delete_registry.empty:

        st.info(
            "There are no Data Entities available to delete."
        )

    else:

        entity_options = (
            delete_registry[
                ["entity_id", "entity_name"]
            ]
            .drop_duplicates()
            .sort_values("entity_id")
        )

        entity_options["display_name"] = (
            entity_options["entity_id"].astype(str)
            + " — "
            + entity_options["entity_name"].astype(str)
        )

        selected_entity = st.selectbox(
            "Select Data Entity to delete",
            entity_options["display_name"].tolist(),
            key="delete_entity_selection"
        )

        selected_row = entity_options[
            entity_options["display_name"] == selected_entity
        ].iloc[0]

        selected_entity_id = selected_row["entity_id"]

        if st.button(
            "Delete Data Entity",
            key="delete_entity"
        ):

            deleted = delete_owner_registry(
                selected_entity_id
            )

            if deleted:

                st.success(
                    f"Entity '{selected_entity_id}' "
                    "was deleted successfully."
                )

                st.rerun()

            else:

                st.warning(
                    f"Entity '{selected_entity_id}' "
                    "was not found."
                )


    st.divider()


    # ========================================================
    # ADD NEW DATA ENTITY
    # ========================================================

    with st.expander(
        "Add New Data Entity"
    ):

        st.subheader("Entity Information")

        col1, col2 = st.columns(2)

        with col1:

            entity_id = st.text_input(
                "Entity ID *",
                placeholder="Example: ENT-001"
            )

        with col2:

            entity_name = st.text_input(
                "Entity Name *",
                placeholder="Example: Customer"
            )

        description = st.text_area(
            "Description",
            placeholder="Describe the data entity."
        )

        col1, col2 = st.columns(2)

        with col1:

            data_domain = st.text_input(
                "Data Domain *",
                placeholder="Example: Customer"
            )

        with col2:

            data_classification = st.selectbox(
                "Data Classification *",
                [
                    "Public",
                    "Internal",
                    "Confidential",
                    "Restricted"
                ]
            )


        # ====================================================
        # OWNERSHIP ASSIGNMENTS
        # ====================================================

        st.subheader("Ownership Assignments")

        owner_count = st.number_input(
            "Number of Ownership Assignments",
            min_value=1,
            max_value=8,
            value=1,
            step=1
        )

        ownership_assignments = []

        for number in range(1, owner_count + 1):

            st.markdown(
                f"**Ownership Assignment {number}**"
            )

            col1, col2 = st.columns(2)

            with col1:

                ownership_scope = st.text_input(
                    "Ownership Scope",
                    key=f"ownership_scope_{number}",
                    placeholder="Example: Retail Banking"
                )

            with col2:

                program = st.text_input(
                    "Program",
                    key=f"program_{number}",
                    placeholder="Example: Customer Program"
                )

            col1, col2 = st.columns(2)

            with col1:

                owner_division_head = st.text_input(
                    "Data Owner - Division Head",
                    key=f"owner_division_head_{number}"
                )

            with col2:

                owner_division = st.text_input(
                    "Data Owner Division",
                    key=f"owner_division_{number}"
                )

            col1, col2 = st.columns(2)

            with col1:

                owner_department_head = st.text_input(
                    "Data Owner - Department Head",
                    key=f"owner_department_head_{number}"
                )

            with col2:

                owner_department = st.text_input(
                    "Data Owner Department",
                    key=f"owner_department_{number}"
                )

            ownership_assignments.append(
                {
                    "ownership_scope": ownership_scope,
                    "program": program,
                    "data_owner_division_head":
                        owner_division_head,
                    "data_owner_division":
                        owner_division,
                    "data_owner_department_head":
                        owner_department_head,
                    "data_owner_department":
                        owner_department
                }
            )


        # ====================================================
        # DATA STEWARDS
        # ====================================================

        st.subheader("Data Stewards")

        steward_count = st.number_input(
            "Number of Data Stewards",
            min_value=1,
            max_value=3,
            value=1,
            step=1
        )

        stewards = []

        for number in range(1, steward_count + 1):

            st.markdown(
                f"**Data Steward {number}**"
            )

            col1, col2 = st.columns(2)

            with col1:

                division_head = st.text_input(
                    "Name (Division Head)",
                    key=f"steward_division_head_{number}"
                )

            with col2:

                division = st.text_input(
                    "Division",
                    key=f"steward_division_{number}"
                )

            col1, col2 = st.columns(2)

            with col1:

                department_head = st.text_input(
                    "Name (Department Head)",
                    key=f"steward_department_head_{number}"
                )

            with col2:

                department = st.text_input(
                    "Department",
                    key=f"steward_department_{number}"
                )

            stewards.append(
                {
                    "division_head": division_head,
                    "division": division,
                    "department_head": department_head,
                    "department": department
                }
            )


        # ====================================================
        # DATA CUSTODIANS
        # ====================================================

        st.subheader("Data Custodians")

        custodian_count = st.number_input(
            "Number of Data Custodians",
            min_value=1,
            max_value=3,
            value=1,
            step=1
        )

        custodians = []

        for number in range(1, custodian_count + 1):

            st.markdown(
                f"**Data Custodian {number}**"
            )

            col1, col2 = st.columns(2)

            with col1:

                division_head = st.text_input(
                    "Name (Division Head)",
                    key=f"custodian_division_head_{number}"
                )

            with col2:

                division = st.text_input(
                    "Division",
                    key=f"custodian_division_{number}"
                )

            col1, col2 = st.columns(2)

            with col1:

                department_head = st.text_input(
                    "Name (Department Head)",
                    key=f"custodian_department_head_{number}"
                )

            with col2:

                department = st.text_input(
                    "Department",
                    key=f"custodian_department_{number}"
                )

            custodians.append(
                {
                    "division_head": division_head,
                    "division": division,
                    "department_head": department_head,
                    "department": department
                }
            )


        # ====================================================
        # SAVE DATA ENTITY
        # ====================================================

        if st.button(
            "Save Data Entity",
            key="save_data_entity"
        ):

            validation_errors = []

            if not entity_id.strip():

                validation_errors.append(
                    "Entity ID is required."
                )

            if not entity_name.strip():

                validation_errors.append(
                    "Entity Name is required."
                )

            if not data_domain.strip():

                validation_errors.append(
                    "Data Domain is required."
                )


            # ------------------------------------------------
            # Validate ownership assignments.
            # ------------------------------------------------

            for number, assignment in enumerate(
                ownership_assignments,
                start=1
            ):

                if not assignment[
                    "ownership_scope"
                ].strip():

                    validation_errors.append(
                        f"Ownership Scope is required "
                        f"for Ownership Assignment {number}."
                    )


            if validation_errors:

                st.error(
                    "Please correct the following:"
                )

                for error in validation_errors:

                    st.write(
                        f"• {error}"
                    )

            else:

                try:

                    while len(stewards) < 3:

                        stewards.append(
                            {
                                "division_head": "",
                                "division": "",
                                "department_head": "",
                                "department": ""
                            }
                        )

                    while len(custodians) < 3:

                        custodians.append(
                            {
                                "division_head": "",
                                "division": "",
                                "department_head": "",
                                "department": ""
                            }
                        )

                    first_owner = ownership_assignments[0]

                    save_owner_registry(

                        entity_id.strip(),
                        entity_name.strip(),
                        description.strip(),
                        data_domain.strip(),
                        data_classification,

                        first_owner[
                            "data_owner_division_head"
                        ].strip(),

                        first_owner[
                            "data_owner_division"
                        ].strip(),

                        first_owner[
                            "data_owner_department_head"
                        ].strip(),

                        first_owner[
                            "data_owner_department"
                        ].strip(),

                        # Steward 1
                        stewards[0]["division_head"],
                        stewards[0]["division"],
                        stewards[0]["department_head"],
                        stewards[0]["department"],

                        # Steward 2
                        stewards[1]["division_head"],
                        stewards[1]["division"],
                        stewards[1]["department_head"],
                        stewards[1]["department"],

                        # Steward 3
                        stewards[2]["division_head"],
                        stewards[2]["division"],
                        stewards[2]["department_head"],
                        stewards[2]["department"],

                        # Custodian 1
                        custodians[0]["division_head"],
                        custodians[0]["division"],
                        custodians[0]["department_head"],
                        custodians[0]["department"],

                        # Custodian 2
                        custodians[1]["division_head"],
                        custodians[1]["division"],
                        custodians[1]["department_head"],
                        custodians[1]["department"],

                        # Custodian 3
                        custodians[2]["division_head"],
                        custodians[2]["division"],
                        custodians[2]["department_head"],
                        custodians[2]["department"]
                    )


                    # ----------------------------------------
                    # Save ownership assignments.
                    # ----------------------------------------

                    for assignment in ownership_assignments:

                        save_ownership_assignment(

                            entity_id.strip(),

                            assignment[
                                "ownership_scope"
                            ].strip(),

                            assignment[
                                "program"
                            ].strip(),

                            assignment[
                                "data_owner_division_head"
                            ].strip(),

                            assignment[
                                "data_owner_division"
                            ].strip(),

                            assignment[
                                "data_owner_department_head"
                            ].strip(),

                            assignment[
                                "data_owner_department"
                            ].strip()
                        )


                    st.success(
                        "Data Entity saved successfully."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to save Data Entity: {error}"
                    )


    st.divider()


    # ========================================================
    # BULK CSV IMPORT
    # ========================================================

    with st.expander(
        "Bulk Import"
    ):

        st.write(
            "Upload a CSV file to add Data Owner Registry information."
        )

        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            key="owner_registry_csv"
        )

        if uploaded_file is not None:

            try:

                uploaded_dataframe = pd.read_csv(
                    uploaded_file
                )

                st.subheader("CSV Preview")

                st.dataframe(
                    uploaded_dataframe,
                    use_container_width=True,
                    hide_index=True
                )

                st.write(
                    f"Rows: {len(uploaded_dataframe)} | "
                    f"Columns: {len(uploaded_dataframe.columns)}"
                )

                if st.button(
                    "Import CSV",
                    key="import_owner_registry"
                ):

                    result = import_owner_registry_from_csv(
                        uploaded_dataframe
                    )

                    if result.get("success"):

                        st.success(
                            "CSV import completed successfully."
                        )

                        st.write(
                            f"Data Entities imported: "
                            f"{result.get('imported_entities', 0)}"
                        )

                        st.write(
                            f"Ownership Assignments imported: "
                            f"{result.get('imported_assignments', 0)}"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "CSV import could not be completed."
                        )

                        errors = result.get(
                            "errors",
                            []
                        )

                        if errors:

                            st.write(
                                "Import errors:"
                            )

                            for error in errors:

                                st.error(
                                    str(error)
                                )

                        else:

                            st.error(
                                "The import failed, but no "
                                "additional error details were returned."
                            )

            except Exception as error:

                st.error(
                    f"Unable to read the CSV file: {error}"
                )


# ============================================================
# DATA CATALOG
# ============================================================

elif page == "Data Catalog":

    st.title("Data Catalog")

    st.write(
        "Data Catalog functionality will be developed here."
    )


# ============================================================
# CLASSIFICATION ENGINE
# ============================================================

elif page == "Classification Engine":

    st.title("Classification Engine")

    st.write(
        "Data Classification Engine functionality "
        "will be developed here."
    )


# ============================================================
# CDE IDENTIFICATION TOOL
# ============================================================

elif page == "CDE Identification Tool":

    st.title("CDE Identification Tool")

    st.write(
        "Assess whether a data element should be considered "
        "a Critical Data Element (CDE)."
    )

    st.info(
        "Use this tool to assess the business importance, "
        "regulatory impact, risk impact, customer impact "
        "and enterprise usage of a data element."
    )

    st.divider()

    # ------------------------------------------------------------
    # DATA ELEMENT INFORMATION
    # ------------------------------------------------------------

    with st.expander(
        "1. Data Element Information",
        expanded=True
    ):

        st.subheader("Data Element")

        col1, col2 = st.columns(2)

        with col1:
            assessment_cde = st.text_input(
                "Data Element / CDE Name *",
                placeholder="Example: Customer ID",
                key="assessment_cde"
            )

        with col2:
            assessment_attribute = st.text_input(
                "Attribute *",
                placeholder="Example: Customer_ID",
                key="assessment_attribute"
            )

        assessment_description = st.text_area(
            "Data Element Description *",
            placeholder=(
                "Describe what this data element represents "
                "and how it is used."
            ),
            key="assessment_description"
        )

        col1, col2 = st.columns(2)

        with col1:
            assessment_data_domain = st.text_input(
                "Data Domain / Entity *",
                placeholder="Example: Customer",
                key="assessment_data_domain"
            )

        with col2:
            assessment_system = st.text_input(
                "System of Record",
                placeholder="Example: CRM",
                key="assessment_system"
            )

        assessment_classification = st.selectbox(
            "Data Classification",
            [
                "Public",
                "Internal",
                "Confidential",
                "Restricted"
            ],
            key="assessment_classification"
        )

    # ------------------------------------------------------------
    # BUSINESS CONTEXT
    # ------------------------------------------------------------

    with st.expander(
        "2. Business Context",
        expanded=True
    ):

        st.subheader("How is this data element used?")

        business_use = st.text_area(
            "Business Usage",
            placeholder=(
                "Describe the key business processes, "
                "reports, decisions or activities that use "
                "this data element."
            ),
            key="assessment_business_use"
        )

        col1, col2 = st.columns(2)

        with col1:
            critical_process = st.selectbox(
                "Used in a Critical Business Process?",
                [
                    "Yes",
                    "No",
                    "Unknown"
                ],
                key="assessment_critical_process"
            )

        with col2:
            enterprise_usage = st.selectbox(
                "Used Across Multiple Business Areas?",
                [
                    "Yes",
                    "No",
                    "Unknown"
                ],
                key="assessment_enterprise_usage"
            )

        col1, col2 = st.columns(2)

        with col1:
            decision_making = st.selectbox(
                "Used for Important Business Decisions?",
                [
                    "Yes",
                    "No",
                    "Unknown"
                ],
                key="assessment_decision_making"
            )

        with col2:
            management_reporting = st.selectbox(
                "Used in Management Reporting / KPI?",
                [
                    "Yes",
                    "No",
                    "Unknown"
                ],
                key="assessment_management_reporting"
            )

    # ------------------------------------------------------------
    # CDE ASSESSMENT CRITERIA
    # ------------------------------------------------------------

    with st.expander(
        "3. CDE Assessment Criteria",
        expanded=True
    ):

        st.write(
            "For each criterion, indicate whether the "
            "data element meets the condition."
        )

        st.subheader("Regulatory & Compliance")

        regulatory_requirement = st.selectbox(
            "Is the data element required by a law, "
            "regulation or regulatory requirement?",
            [
                "Yes",
                "No",
                "Unknown"
            ],
            key="assessment_regulatory"
        )

        regulatory_reporting = st.selectbox(
            "Is the data element used in regulatory reporting?",
            [
                "Yes",
                "No",
                "Unknown"
            ],
            key="assessment_regulatory_reporting"
        )

        st.subheader("Financial Impact")

        financial_impact = st.selectbox(
            "Could incorrect data materially affect "
            "financial reporting or financial results?",
            [
                "Yes",
                "No",
                "Unknown"
            ],
            key="assessment_financial"
        )

        st.subheader("Risk & Compliance Impact")

        risk_impact = st.selectbox(
            "Could incorrect data create significant "
            "business, regulatory, financial or operational risk?",
            [
                "Yes",
                "No",
                "Unknown"
            ],
            key="assessment_risk"
        )

        st.subheader("Customer Impact")

        customer_impact = st.selectbox(
            "Could incorrect data materially affect "
            "customer identification, servicing, eligibility "
            "or customer decisions?",
            [
                "Yes",
                "No",
                "Unknown"
            ],
            key="assessment_customer"
        )

        st.subheader("Data Quality Impact")

        data_quality_impact = st.selectbox(
            "Would poor quality of this data materially "
            "affect downstream processes, reporting or decisions?",
            [
                "Yes",
                "No",
                "Unknown"
            ],
            key="assessment_data_quality"
        )

        st.subheader("Enterprise Importance")

        enterprise_importance = st.selectbox(
            "Is this data element widely used across "
            "the organization or multiple systems?",
            [
                "Yes",
                "No",
                "Unknown"
            ],
            key="assessment_enterprise_importance"
        )

    # ------------------------------------------------------------
    # ASSESSMENT NOTES
    # ------------------------------------------------------------

    with st.expander(
        "4. Assessment Notes",
        expanded=True
    ):

        assessment_notes = st.text_area(
            "Assessment Notes",
            placeholder=(
                "Provide any additional information that "
                "supports the assessment."
            ),
            key="assessment_notes"
        )

        assessment_reviewer = st.text_input(
            "Assessment Performed By",
            placeholder="Name / Role",
            key="assessment_reviewer"
        )

    # ------------------------------------------------------------
    # RUN CDE ASSESSMENT
    #
    # IMPORTANT:
    # The result is stored in session_state so it remains visible
    # after Streamlit reruns when the governance button is clicked.
    # ------------------------------------------------------------

    st.divider()

    st.subheader("CDE Assessment")

    if st.button(
        "Run CDE Assessment",
        key="submit_cde_assessment"
    ):

        validation_errors = []

        if not assessment_cde.strip():
            validation_errors.append(
                "Data Element / CDE Name is required."
            )

        if not assessment_attribute.strip():
            validation_errors.append(
                "Attribute is required."
            )

        if not assessment_description.strip():
            validation_errors.append(
                "Data Element Description is required."
            )

        if not assessment_data_domain.strip():
            validation_errors.append(
                "Data Domain / Entity is required."
            )

        if validation_errors:

            st.error(
                "Please complete the required information:"
            )

            for error in validation_errors:
                st.write(f"• {error}")

            st.session_state["cde_assessment_ready"] = False

        else:

            criteria = [
                (
                    "Regulatory requirement",
                    regulatory_requirement,
                    15
                ),
                (
                    "Regulatory reporting",
                    regulatory_reporting,
                    10
                ),
                (
                    "Financial impact",
                    financial_impact,
                    10
                ),
                (
                    "Risk and compliance impact",
                    risk_impact,
                    15
                ),
                (
                    "Customer impact",
                    customer_impact,
                    10
                ),
                (
                    "Critical business process",
                    critical_process,
                    15
                ),
                (
                    "Important business decision-making",
                    decision_making,
                    5
                ),
                (
                    "Data quality impact",
                    data_quality_impact,
                    5
                ),
                (
                    "Enterprise usage",
                    enterprise_usage,
                    5
                ),
                (
                    "Management reporting / KPI",
                    management_reporting,
                    5
                )
            ]

            total_score = 0
            reasons = []
            unknown_count = 0

            for criterion_name, answer, points in criteria:

                if answer == "Yes":

                    total_score += points

                    reasons.append(
                        f"✓ {criterion_name} identified as significant."
                    )

                elif answer == "Unknown":

                    total_score += points * 0.5
                    unknown_count += 1

                    reasons.append(
                        f"• {criterion_name} requires further confirmation."
                    )

            total_score = int(total_score)

            if total_score >= 70:

                recommendation = "CDE"

                recommendation_message = (
                    "The assessment indicates that this data "
                    "element has a strong likelihood of being "
                    "a Critical Data Element."
                )

            elif total_score >= 40:

                recommendation = "Requires Review"

                recommendation_message = (
                    "The assessment indicates that additional "
                    "governance review is recommended before "
                    "making a final CDE determination."
                )

            else:

                recommendation = "Not CDE"

                recommendation_message = (
                    "The assessment currently indicates that "
                    "this data element does not meet the CDE "
                    "threshold."
                )

            # Store the completed assessment result.
            st.session_state["cde_assessment_ready"] = True
            st.session_state["cde_total_score"] = total_score
            st.session_state["cde_recommendation"] = recommendation
            st.session_state["cde_recommendation_message"] = (
                recommendation_message
            )
            st.session_state["cde_reasons"] = reasons
            st.session_state["cde_unknown_count"] = unknown_count

            st.success(
                "CDE assessment completed. Please review the "
                "result and confirm the governance decision below."
            )

    # ------------------------------------------------------------
    # DISPLAY STORED ASSESSMENT RESULT
    #
    # This section stays INSIDE the CDE Identification Tool page
    # and OUTSIDE the Run button block.
    # ------------------------------------------------------------

    if st.session_state.get(
        "cde_assessment_ready",
        False
    ):

        total_score = st.session_state.get(
            "cde_total_score",
            0
        )

        recommendation = st.session_state.get(
            "cde_recommendation",
            "Not CDE"
        )

        recommendation_message = st.session_state.get(
            "cde_recommendation_message",
            ""
        )

        reasons = st.session_state.get(
            "cde_reasons",
            []
        )

        unknown_count = st.session_state.get(
            "cde_unknown_count",
            0
        )

        st.divider()

        st.subheader("Assessment Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Assessment Score",
                f"{total_score}%"
            )

        with col2:
            st.metric(
                "Recommendation",
                recommendation
            )

        if recommendation == "CDE":

            st.success(
                f"Recommendation: {recommendation}"
            )

        elif recommendation == "Requires Review":

            st.warning(
                f"Recommendation: {recommendation}"
            )

        else:

            st.info(
                f"Recommendation: {recommendation}"
            )

        st.write(
            recommendation_message
        )

        st.subheader("Assessment Rationale")

        if reasons:

            for reason in reasons:
                st.write(reason)

        else:

            st.write(
                "No significant CDE criteria were identified."
            )

        if unknown_count > 0:

            st.warning(
                f"{unknown_count} assessment criterion/"
                f"criteria marked as Unknown. "
                "These should be confirmed during governance review."
            )

        # --------------------------------------------------------
        # GOVERNANCE DECISION
        # --------------------------------------------------------

        st.divider()

        st.subheader("Governance Decision")

        st.write(
            "The assessment recommendation is not the final "
            "governance decision. A governance reviewer should "
            "confirm the final classification."
        )

        governance_decision = st.radio(
            "Select Governance Decision",
            [
                "Confirm as CDE",
                "Requires Review",
                "Do Not Classify as CDE"
            ],
            key="governance_decision"
        )

        governance_rationale = st.text_area(
            "Governance Decision Rationale",
            placeholder=(
                "Explain why the governance decision was made."
            ),
            key="governance_rationale"
        )

        # --------------------------------------------------------
        # SAVE ASSESSMENT
        # --------------------------------------------------------

        if st.button(
            "Confirm Governance Decision",
            key="confirm_governance_decision"
        ):

            if not governance_rationale.strip():

                st.warning(
                    "Please provide a governance decision "
                    "rationale before confirming."
                )

            else:

                assessment_date = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                try:

                    # Step 1:
                    # Save the complete CDE assessment.
                    assessment_id = save_cde_assessment(

                        assessment_date=assessment_date,

                        data_element=assessment_cde.strip(),

                        attribute=assessment_attribute.strip(),

                        description=assessment_description.strip(),

                        data_domain_entity=
                            assessment_data_domain.strip(),

                        system_of_record=
                            assessment_system.strip(),

                        data_classification=
                            assessment_classification,

                        business_usage=
                            business_use.strip(),

                        critical_process=
                            critical_process,

                        enterprise_usage=
                            enterprise_usage,

                        decision_making=
                            decision_making,

                        management_reporting=
                            management_reporting,

                        regulatory_requirement=
                            regulatory_requirement,

                        regulatory_reporting=
                            regulatory_reporting,

                        financial_impact=
                            financial_impact,

                        risk_impact=
                            risk_impact,

                        customer_impact=
                            customer_impact,

                        data_quality_impact=
                            data_quality_impact,

                        enterprise_importance=
                            enterprise_importance,

                        assessment_notes=
                            assessment_notes.strip(),

                        assessment_reviewer=
                            assessment_reviewer.strip(),

                        assessment_score=
                            total_score,

                        recommendation=
                            recommendation,

                        governance_decision=
                            governance_decision,

                        governance_rationale=
                            governance_rationale.strip()
                    )

                    # Step 2:
                    # If governance confirms this as a CDE,
                    # automatically add it to the CDE Registry.
                    if governance_decision == "Confirm as CDE":

                        cde_reference_id = (
                            f"CDE-{assessment_id:05d}"
                        )

                        save_cde(

                            cde_reference_id,

                            assessment_cde.strip(),

                            assessment_attribute.strip(),

                            assessment_description.strip(),

                            assessment_data_domain.strip(),

                            assessment_system.strip(),

                            assessment_classification,

                            "Active",

                            assessment_date,

                            assessment_date,

                            "",

                            "",

                            "",

                            "",

                            ""
                        )

                        st.success(
                            "CDE assessment confirmed and "
                            "added to the CDE Registry successfully."
                        )

                        st.write(
                            f"**Assessment ID:** {assessment_id}"
                        )

                        st.write(
                            f"**CDE Reference ID:** "
                            f"{cde_reference_id}"
                        )

                        st.write(
                            f"**Data Element:** "
                            f"{assessment_cde}"
                        )

                        st.write(
                            f"**Attribute:** "
                            f"{assessment_attribute}"
                        )

                        st.write(
                            f"**Assessment Score:** "
                            f"{total_score}%"
                        )

                        st.write(
                            f"**Governance Decision:** "
                            f"{governance_decision}"
                        )

                    # Step 3:
                    # Requires Review does not create a CDE.
                    elif governance_decision == "Requires Review":

                        st.warning(
                            "CDE assessment saved. "
                            "The data element remains under governance "
                            "review and has not been added to the CDE Registry."
                        )

                        st.write(
                            f"**Assessment ID:** {assessment_id}"
                        )

                        st.write(
                            f"**Assessment Score:** "
                            f"{total_score}%"
                        )

                        st.write(
                            f"**Governance Decision:** "
                            f"{governance_decision}"
                        )

                    # Step 4:
                    # Do Not Classify as CDE does not create a CDE.
                    else:

                        st.info(
                            "CDE assessment saved. "
                            "The data element was not classified "
                            "as a Critical Data Element."
                        )

                        st.write(
                            f"**Assessment ID:** {assessment_id}"
                        )

                        st.write(
                            f"**Assessment Score:** "
                            f"{total_score}%"
                        )

                        st.write(
                            f"**Governance Decision:** "
                            f"{governance_decision}"
                        )

                    # Prevent accidental duplicate confirmation
                    # from the same assessment after the save.
                    st.session_state["cde_assessment_ready"] = False

                except Exception as error:

                    st.error(
                        "Unable to save the CDE assessment: "
                        f"{error}"
                    )


# ============================================================
# CDE ENGINE
# ============================================================

elif page == "CDE Engine":

    st.title("Critical Data Element Engine")

    st.write(
        "Manage Critical Data Elements, their attributes, "
        "classification and lifecycle information."
    )

    st.divider()


    # ========================================================
    # CDE DISPLAY LABELS
    # ========================================================

    CDE_LABELS = {

        "id":
            "CDE ID",

        "cde_reference_id":
            "CDE Reference ID",

        "cde":
            "CDE",

        "attribute":
            "Attribute",

        "description":
            "Description",

        "data_domain_entity":
            "Data Domain / Entity",

        "system_of_record":
            "System of Record",

        "data_classification":
            "Data Classification",

        "lifecycle_stage":
            "Lifecycle Stage",

        "date_created":
            "Date Created",

        "date_updated":
            "Date Updated",

        "retention_period":
            "Retention Period",

        "scheduled_archival_date":
            "Scheduled Archival Date",

        "actual_archival_date":
            "Actual Archival Date",

        "scheduled_deletion_date":
            "Scheduled Deletion Date",

        "actual_deletion_date":
            "Actual Deletion Date"
    }


    def prepare_cde_for_display(dataframe):

        dataframe = dataframe.copy()

        dataframe = dataframe.rename(
            columns={
                column: CDE_LABELS[column]
                for column in dataframe.columns
                if column in CDE_LABELS
            }
        )

        return dataframe


    # ========================================================
    # LOAD CDE REGISTRY
    # ========================================================

    cde_registry = get_cde_registry()


    # ========================================================
    # CDE REGISTRY
    # ========================================================

    st.subheader("CDE Registry")

    if cde_registry.empty:

        st.info(
            "No Critical Data Elements have been registered yet."
        )

    else:

        search_cde = st.text_input(
            "Search CDE Registry",
            placeholder=(
                "Search CDE Reference ID, CDE, Attribute, "
                "Data Domain, System of Record..."
            ),
            key="search_cde_registry"
        )


        filtered_cde = cde_registry.copy()


        if search_cde:

            search_cde = search_cde.lower()

            matching_rows = filtered_cde.apply(
                lambda row:
                    row.astype(str)
                    .str.lower()
                    .str.contains(
                        search_cde,
                        na=False
                    )
                    .any(),
                axis=1
            )

            filtered_cde = filtered_cde[
                matching_rows
            ]


        display_cde = prepare_cde_for_display(
            filtered_cde
        )

        st.dataframe(
            display_cde,
            use_container_width=True,
            hide_index=True
        )


    st.divider()


    # ========================================================
    # ADD NEW CDE
    # ========================================================

    with st.expander(
        "Add New CDE"
    ):

        st.subheader("CDE Information")


        col1, col2 = st.columns(2)

        with col1:

            new_cde_reference_id = st.text_input(
                "CDE Reference ID *",
                placeholder="Example: CDE-001",
                key="new_cde_reference_id"
            )

        with col2:

            new_cde = st.text_input(
                "CDE *",
                placeholder="Example: Customer",
                key="new_cde"
            )


        new_attribute = st.text_input(
            "Attribute *",
            placeholder="Example: Customer ID",
            key="new_cde_attribute"
        )


        new_description = st.text_area(
            "Description",
            placeholder=(
                "Describe what this Critical Data Element represents."
            ),
            key="new_cde_description"
        )


        st.subheader("Data Context")

        col1, col2 = st.columns(2)

        with col1:

            new_data_domain_entity = st.text_input(
                "Data Domain / Entity",
                placeholder="Example: Customer",
                key="new_cde_data_domain_entity"
            )

        with col2:

            new_system_of_record = st.text_input(
                "System of Record",
                placeholder="Example: CRM",
                key="new_cde_system_of_record"
            )


        col1, col2 = st.columns(2)

        with col1:

            new_data_classification = st.selectbox(
                "Data Classification *",
                [
                    "Public",
                    "Internal",
                    "Confidential",
                    "Restricted"
                ],
                key="new_cde_data_classification"
            )

        with col2:

            new_lifecycle_stage = st.selectbox(
                "Lifecycle Stage",
                [
                    "Active",
                    "Archived",
                    "Deleted"
                ],
                key="new_cde_lifecycle_stage"
            )


        st.subheader("Lifecycle & Retention")

        col1, col2 = st.columns(2)

        with col1:

            new_date_created = st.text_input(
                "Date Created",
                placeholder="YYYY-MM-DD",
                key="new_cde_date_created"
            )

        with col2:

            new_date_updated = st.text_input(
                "Date Updated",
                placeholder="YYYY-MM-DD",
                key="new_cde_date_updated"
            )


        new_retention_period = st.text_input(
            "Retention Period",
            placeholder="Example: 7 years",
            key="new_cde_retention_period"
        )


        st.subheader("Archival")

        col1, col2 = st.columns(2)

        with col1:

            new_scheduled_archival_date = st.text_input(
                "Scheduled Archival Date",
                placeholder="YYYY-MM-DD",
                key="new_cde_scheduled_archival_date"
            )

        with col2:

            new_actual_archival_date = st.text_input(
                "Actual Archival Date",
                placeholder="YYYY-MM-DD",
                key="new_cde_actual_archival_date"
            )


        st.subheader("Deletion")

        col1, col2 = st.columns(2)

        with col1:

            new_scheduled_deletion_date = st.text_input(
                "Scheduled Deletion Date",
                placeholder="YYYY-MM-DD",
                key="new_cde_scheduled_deletion_date"
            )

        with col2:

            new_actual_deletion_date = st.text_input(
                "Actual Deletion Date",
                placeholder="YYYY-MM-DD",
                key="new_cde_actual_deletion_date"
            )


        if st.button(
            "Save CDE",
            key="save_new_cde"
        ):

            validation_errors = []

            if not new_cde_reference_id.strip():

                validation_errors.append(
                    "CDE Reference ID is required."
                )

            if not new_cde.strip():

                validation_errors.append(
                    "CDE is required."
                )

            if not new_attribute.strip():

                validation_errors.append(
                    "Attribute is required."
                )


            if validation_errors:

                st.error(
                    "Please correct the following:"
                )

                for error in validation_errors:

                    st.write(
                        f"• {error}"
                    )

            else:

                try:

                    save_cde(

                        new_cde_reference_id.strip(),

                        new_cde.strip(),

                        new_attribute.strip(),

                        new_description.strip(),

                        new_data_domain_entity.strip(),

                        new_system_of_record.strip(),

                        new_data_classification,

                        new_lifecycle_stage,

                        new_date_created.strip(),

                        new_date_updated.strip(),

                        new_retention_period.strip(),

                        new_scheduled_archival_date.strip(),

                        new_actual_archival_date.strip(),

                        new_scheduled_deletion_date.strip(),

                        new_actual_deletion_date.strip()
                    )


                    st.success(
                        "CDE created successfully."
                    )

                    st.rerun()


                except Exception as error:

                    st.error(
                        f"Unable to save CDE: {error}"
                    )


    st.divider()


    # ========================================================
    # EDIT CDE
    # ========================================================

    with st.expander(
        "Edit CDE"
    ):

        edit_registry = get_cde_registry()


        if edit_registry.empty:

            st.info(
                "There are no CDE records available to edit."
            )

        else:

            edit_registry = edit_registry.copy()

            edit_registry["display_name"] = (
                edit_registry["cde_reference_id"]
                .astype(str)
                + " — "
                + edit_registry["cde"]
                .astype(str)
                + " — "
                + edit_registry["attribute"]
                .astype(str)
            )


            selected_edit_cde = st.selectbox(
                "Select CDE to edit",
                edit_registry[
                    "display_name"
                ].tolist(),
                key="edit_cde_selection"
            )


            selected_edit_row = edit_registry[
                edit_registry["display_name"]
                == selected_edit_cde
            ].iloc[0]


            selected_cde_id = int(
                selected_edit_row["id"]
            )


            st.subheader(
                "Edit CDE Information"
            )


            col1, col2 = st.columns(2)

            with col1:

                edit_cde_reference_id = st.text_input(
                    "CDE Reference ID *",
                    value=str(
                        selected_edit_row[
                            "cde_reference_id"
                        ]
                    ),
                    key="edit_cde_reference_id"
                )

            with col2:

                edit_cde = st.text_input(
                    "CDE *",
                    value=str(
                        selected_edit_row["cde"]
                    ),
                    key="edit_cde"
                )


            edit_attribute = st.text_input(
                "Attribute *",
                value=str(
                    selected_edit_row["attribute"]
                ),
                key="edit_cde_attribute"
            )


            edit_description = st.text_area(
                "Description",
                value=str(
                    selected_edit_row["description"]
                ),
                key="edit_cde_description"
            )


            st.subheader("Data Context")

            col1, col2 = st.columns(2)

            with col1:

                edit_data_domain_entity = st.text_input(
                    "Data Domain / Entity",
                    value=str(
                        selected_edit_row[
                            "data_domain_entity"
                        ]
                    ),
                    key="edit_cde_data_domain_entity"
                )

            with col2:

                edit_system_of_record = st.text_input(
                    "System of Record",
                    value=str(
                        selected_edit_row[
                            "system_of_record"
                        ]
                    ),
                    key="edit_cde_system_of_record"
                )


            classification_options = [
                "Public",
                "Internal",
                "Confidential",
                "Restricted"
            ]

            current_classification = str(
                selected_edit_row[
                    "data_classification"
                ]
            )

            if current_classification not in classification_options:

                classification_options.append(
                    current_classification
                )


            lifecycle_options = [
                "Active",
                "Archived",
                "Deleted"
            ]

            current_lifecycle = str(
                selected_edit_row[
                    "lifecycle_stage"
                ]
            )

            if current_lifecycle not in lifecycle_options:

                lifecycle_options.append(
                    current_lifecycle
                )


            col1, col2 = st.columns(2)

            with col1:

                edit_data_classification = st.selectbox(
                    "Data Classification *",
                    classification_options,
                    index=classification_options.index(
                        current_classification
                    ),
                    key="edit_cde_data_classification"
                )

            with col2:

                edit_lifecycle_stage = st.selectbox(
                    "Lifecycle Stage",
                    lifecycle_options,
                    index=lifecycle_options.index(
                        current_lifecycle
                    ),
                    key="edit_cde_lifecycle_stage"
                )


            st.subheader("Lifecycle & Retention")

            col1, col2 = st.columns(2)

            with col1:

                edit_date_created = st.text_input(
                    "Date Created",
                    value=str(
                        selected_edit_row[
                            "date_created"
                        ]
                    ),
                    key="edit_cde_date_created"
                )

            with col2:

                edit_date_updated = st.text_input(
                    "Date Updated",
                    value=str(
                        selected_edit_row[
                            "date_updated"
                        ]
                    ),
                    key="edit_cde_date_updated"
                )


            edit_retention_period = st.text_input(
                "Retention Period",
                value=str(
                    selected_edit_row[
                        "retention_period"
                    ]
                ),
                key="edit_cde_retention_period"
            )


            st.subheader("Archival")

            col1, col2 = st.columns(2)

            with col1:

                edit_scheduled_archival_date = st.text_input(
                    "Scheduled Archival Date",
                    value=str(
                        selected_edit_row[
                            "scheduled_archival_date"
                        ]
                    ),
                    key="edit_cde_scheduled_archival_date"
                )

            with col2:

                edit_actual_archival_date = st.text_input(
                    "Actual Archival Date",
                    value=str(
                        selected_edit_row[
                            "actual_archival_date"
                        ]
                    ),
                    key="edit_cde_actual_archival_date"
                )


            st.subheader("Deletion")

            col1, col2 = st.columns(2)

            with col1:

                edit_scheduled_deletion_date = st.text_input(
                    "Scheduled Deletion Date",
                    value=str(
                        selected_edit_row[
                            "scheduled_deletion_date"
                        ]
                    ),
                    key="edit_cde_scheduled_deletion_date"
                )

            with col2:

                edit_actual_deletion_date = st.text_input(
                    "Actual Deletion Date",
                    value=str(
                        selected_edit_row[
                            "actual_deletion_date"
                        ]
                    ),
                    key="edit_cde_actual_deletion_date"
                )


            if st.button(
                "Update CDE",
                key="update_cde"
            ):

                validation_errors = []

                if not edit_cde_reference_id.strip():

                    validation_errors.append(
                        "CDE Reference ID is required."
                    )

                if not edit_cde.strip():

                    validation_errors.append(
                        "CDE is required."
                    )

                if not edit_attribute.strip():

                    validation_errors.append(
                        "Attribute is required."
                    )


                if validation_errors:

                    st.error(
                        "Please correct the following:"
                    )

                    for error in validation_errors:

                        st.write(
                            f"• {error}"
                        )


                else:

                    try:

                        updated = update_cde(

                            selected_cde_id,

                            edit_cde_reference_id.strip(),

                            edit_cde.strip(),

                            edit_attribute.strip(),

                            edit_description.strip(),

                            edit_data_domain_entity.strip(),

                            edit_system_of_record.strip(),

                            edit_data_classification,

                            edit_lifecycle_stage,

                            edit_date_created.strip(),

                            edit_date_updated.strip(),

                            edit_retention_period.strip(),

                            edit_scheduled_archival_date.strip(),

                            edit_actual_archival_date.strip(),

                            edit_scheduled_deletion_date.strip(),

                            edit_actual_deletion_date.strip()
                        )


                        if updated:

                            st.success(
                                "CDE updated successfully."
                            )

                            st.rerun()

                        else:

                            st.warning(
                                "The selected CDE could not be updated."
                            )


                    except Exception as error:

                        st.error(
                            f"Unable to update CDE: {error}"
                        )


    st.divider()


    # ========================================================
    # DELETE CDE
    # ========================================================

    with st.expander(
        "Delete CDE"
    ):

        delete_registry = get_cde_registry()


        if delete_registry.empty:

            st.info(
                "There are no CDE records available to delete."
            )

        else:

            delete_registry = delete_registry.copy()

            delete_registry["display_name"] = (
                delete_registry["cde_reference_id"]
                .astype(str)
                + " — "
                + delete_registry["cde"]
                .astype(str)
                + " — "
                + delete_registry["attribute"]
                .astype(str)
            )


            selected_delete_cde = st.selectbox(
                "Select CDE to delete",
                delete_registry[
                    "display_name"
                ].tolist(),
                key="delete_cde_selection"
            )


            selected_delete_row = delete_registry[
                delete_registry["display_name"]
                == selected_delete_cde
            ].iloc[0]


            selected_delete_cde_id = int(
                selected_delete_row["id"]
            )


            st.warning(
                "Deleting a CDE is permanent."
            )


            if st.button(
                "Delete CDE",
                key="delete_cde"
            ):

                try:

                    deleted = delete_cde(
                        selected_delete_cde_id
                    )


                    if deleted:

                        st.success(
                            "CDE deleted successfully."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "The selected CDE could not be deleted."
                        )


                except Exception as error:

                    st.error(
                        f"Unable to delete CDE: {error}"
                    )


# ============================================================
# POLICIES & STANDARDS
# ============================================================

elif page == "Policies & Standards":

    st.title("Policies & Standards")

    st.write(
        "Policies and Data Governance Standards "
        "will be managed here."
    )