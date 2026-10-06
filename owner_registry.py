
# ============================================================
# owner_registry.py
# ============================================================
# Data Owner Registry + CDE Registry database functions
# ============================================================

import sqlite3
import pandas as pd

from database import get_connection


# ============================================================
# HELPER
# ============================================================

def clean_csv_value(value):
    """
    Convert CSV values into clean text.

    Blank values become an empty string.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


# ============================================================
# DATA OWNER REGISTRY
# ============================================================

def save_owner_registry(
    entity_id,
    entity_name,
    description,
    data_domain,
    data_classification,

    data_owner_division_head,
    data_owner_division,
    data_owner_department_head,
    data_owner_department,

    data_steward_1_division_head,
    data_steward_1_division,
    data_steward_1_department_head,
    data_steward_1_department,

    data_steward_2_division_head,
    data_steward_2_division,
    data_steward_2_department_head,
    data_steward_2_department,

    data_steward_3_division_head,
    data_steward_3_division,
    data_steward_3_department_head,
    data_steward_3_department,

    data_custodian_1_division_head,
    data_custodian_1_division,
    data_custodian_1_department_head,
    data_custodian_1_department,

    data_custodian_2_division_head,
    data_custodian_2_division,
    data_custodian_2_department_head,
    data_custodian_2_department,

    data_custodian_3_division_head,
    data_custodian_3_division,
    data_custodian_3_department_head,
    data_custodian_3_department
):
    """
    Save one Data Entity into the Data Owner Registry.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO data_owner_registry (

            entity_id,
            entity_name,
            description,
            data_domain,
            data_classification,

            data_owner_division_head,
            data_owner_division,
            data_owner_department_head,
            data_owner_department,

            data_steward_1_division_head,
            data_steward_1_division,
            data_steward_1_department_head,
            data_steward_1_department,

            data_steward_2_division_head,
            data_steward_2_division,
            data_steward_2_department_head,
            data_steward_2_department,

            data_steward_3_division_head,
            data_steward_3_division,
            data_steward_3_department_head,
            data_steward_3_department,

            data_custodian_1_division_head,
            data_custodian_1_division,
            data_custodian_1_department_head,
            data_custodian_1_department,

            data_custodian_2_division_head,
            data_custodian_2_division,
            data_custodian_2_department_head,
            data_custodian_2_department,

            data_custodian_3_division_head,
            data_custodian_3_division,
            data_custodian_3_department_head,
            data_custodian_3_department

        )

        VALUES (

            ?, ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?, ?

        )
        """,
        (
            entity_id,
            entity_name,
            description,
            data_domain,
            data_classification,

            data_owner_division_head,
            data_owner_division,
            data_owner_department_head,
            data_owner_department,

            data_steward_1_division_head,
            data_steward_1_division,
            data_steward_1_department_head,
            data_steward_1_department,

            data_steward_2_division_head,
            data_steward_2_division,
            data_steward_2_department_head,
            data_steward_2_department,

            data_steward_3_division_head,
            data_steward_3_division,
            data_steward_3_department_head,
            data_steward_3_department,

            data_custodian_1_division_head,
            data_custodian_1_division,
            data_custodian_1_department_head,
            data_custodian_1_department,

            data_custodian_2_division_head,
            data_custodian_2_division,
            data_custodian_2_department_head,
            data_custodian_2_department,

            data_custodian_3_division_head,
            data_custodian_3_division,
            data_custodian_3_department_head,
            data_custodian_3_department
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# GET BASIC REGISTRY
# ============================================================

def get_registry():

    connection = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT *
        FROM data_owner_registry
        ORDER BY entity_id
        """,
        connection
    )

    connection.close()

    return dataframe


# ============================================================
# DELETE DATA ENTITY
# ============================================================

def delete_owner_registry(entity_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM data_owner_registry
        WHERE entity_id = ?
        """,
        (entity_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()

    connection.close()

    return deleted


# ============================================================
# OWNERSHIP ASSIGNMENTS
# ============================================================

def save_ownership_assignment(
    entity_id,
    ownership_scope,
    program,
    data_owner_division_head,
    data_owner_division,
    data_owner_department_head,
    data_owner_department
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO ownership_assignments (

            entity_id,
            ownership_scope,
            program,
            data_owner_division_head,
            data_owner_division,
            data_owner_department_head,
            data_owner_department

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entity_id,
            ownership_scope,
            program,
            data_owner_division_head,
            data_owner_division,
            data_owner_department_head,
            data_owner_department
        )
    )

    connection.commit()

    connection.close()


def get_ownership_assignments(entity_id=None):

    connection = get_connection()

    if entity_id:

        dataframe = pd.read_sql_query(
            """
            SELECT *
            FROM ownership_assignments
            WHERE entity_id = ?
            ORDER BY id
            """,
            connection,
            params=(entity_id,)
        )

    else:

        dataframe = pd.read_sql_query(
            """
            SELECT *
            FROM ownership_assignments
            ORDER BY entity_id, id
            """,
            connection
        )

    connection.close()

    return dataframe


# ============================================================
# COMPLETE OWNER REGISTRY
# ============================================================

def get_complete_owner_registry():

    connection = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT

            dor.entity_id,
            dor.entity_name,
            dor.description,
            dor.data_domain,
            dor.data_classification,

            oa.id AS ownership_assignment_id,
            oa.ownership_scope,
            oa.program,

            oa.data_owner_division_head,
            oa.data_owner_division,
            oa.data_owner_department_head,
            oa.data_owner_department,

            dor.data_steward_1_division_head,
            dor.data_steward_1_division,
            dor.data_steward_1_department_head,
            dor.data_steward_1_department,

            dor.data_steward_2_division_head,
            dor.data_steward_2_division,
            dor.data_steward_2_department_head,
            dor.data_steward_2_department,

            dor.data_steward_3_division_head,
            dor.data_steward_3_division,
            dor.data_steward_3_department_head,
            dor.data_steward_3_department,

            dor.data_custodian_1_division_head,
            dor.data_custodian_1_division,
            dor.data_custodian_1_department_head,
            dor.data_custodian_1_department,

            dor.data_custodian_2_division_head,
            dor.data_custodian_2_division,
            dor.data_custodian_2_department_head,
            dor.data_custodian_2_department,

            dor.data_custodian_3_division_head,
            dor.data_custodian_3_division,
            dor.data_custodian_3_department_head,
            dor.data_custodian_3_department

        FROM data_owner_registry dor

        LEFT JOIN ownership_assignments oa
            ON dor.entity_id = oa.entity_id

        ORDER BY
            dor.entity_id,
            oa.id
        """,
        connection
    )

    connection.close()

    return dataframe


# ============================================================
# CSV IMPORT
# ============================================================

def import_owner_registry_from_csv(dataframe):

    required_columns = [

        "Entity ID",
        "Entity Name",
        "Data Domain",
        "Data Classification",

        "Ownership Assignment ID",
        "Ownership Scope",

        "Data Owner - Division Head",
        "Data Owner Division",
        "Data Owner - Department Head",
        "Data Owner Department"
    ]

    errors = []

    for column in required_columns:

        if column not in dataframe.columns:

            errors.append(
                f"Missing required column: {column}"
            )

    if errors:

        return {
            "success": False,
            "imported_entities": 0,
            "imported_assignments": 0,
            "skipped_rows": 0,
            "errors": errors
        }


    connection = get_connection()

    cursor = connection.cursor()

    imported_entities = 0
    imported_assignments = 0
    skipped_rows = 0

    processed_entities = set()
    assignment_ids = set()

    try:

        for _, row in dataframe.iterrows():

            entity_id = clean_csv_value(
                row["Entity ID"]
            )

            entity_name = clean_csv_value(
                row["Entity Name"]
            )

            data_domain = clean_csv_value(
                row["Data Domain"]
            )

            data_classification = clean_csv_value(
                row["Data Classification"]
            )

            ownership_assignment_id = clean_csv_value(
                row["Ownership Assignment ID"]
            )

            ownership_scope = clean_csv_value(
                row["Ownership Scope"]
            )

            owner_division_head = clean_csv_value(
                row["Data Owner - Division Head"]
            )

            owner_division = clean_csv_value(
                row["Data Owner Division"]
            )

            owner_department_head = clean_csv_value(
                row["Data Owner - Department Head"]
            )

            owner_department = clean_csv_value(
                row["Data Owner Department"]
            )


            if not entity_id:

                errors.append(
                    "Entity ID is required."
                )

                skipped_rows += 1

                continue


            if not entity_name:

                errors.append(
                    f"Entity Name is required for {entity_id}."
                )

                skipped_rows += 1

                continue


            if not data_domain:

                errors.append(
                    f"Data Domain is required for {entity_id}."
                )

                skipped_rows += 1

                continue


            if not data_classification:

                errors.append(
                    f"Data Classification is required for {entity_id}."
                )

                skipped_rows += 1

                continue


            if not ownership_assignment_id:

                errors.append(
                    f"Ownership Assignment ID is required "
                    f"for {entity_id}."
                )

                skipped_rows += 1

                continue


            if ownership_assignment_id in assignment_ids:

                errors.append(
                    f"Duplicate Ownership Assignment ID: "
                    f"{ownership_assignment_id}"
                )

                skipped_rows += 1

                continue


            assignment_ids.add(
                ownership_assignment_id
            )


            # ------------------------------------------------
            # Save entity only once.
            # ------------------------------------------------

            if entity_id not in processed_entities:

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO data_owner_registry (

                        entity_id,
                        entity_name,
                        description,
                        data_domain,
                        data_classification,

                        data_owner_division_head,
                        data_owner_division,
                        data_owner_department_head,
                        data_owner_department,

                        data_steward_1_division_head,
                        data_steward_1_division,
                        data_steward_1_department_head,
                        data_steward_1_department,

                        data_steward_2_division_head,
                        data_steward_2_division,
                        data_steward_2_department_head,
                        data_steward_2_department,

                        data_steward_3_division_head,
                        data_steward_3_division,
                        data_steward_3_department_head,
                        data_steward_3_department,

                        data_custodian_1_division_head,
                        data_custodian_1_division,
                        data_custodian_1_department_head,
                        data_custodian_1_department,

                        data_custodian_2_division_head,
                        data_custodian_2_division,
                        data_custodian_2_department_head,
                        data_custodian_2_department,

                        data_custodian_3_division_head,
                        data_custodian_3_division,
                        data_custodian_3_department_head,
                        data_custodian_3_department

                    )

                    VALUES (

                        ?, ?, ?, ?, ?,

                        ?, ?, ?, ?,

                        ?, ?, ?, ?,

                        ?, ?, ?, ?,

                        ?, ?, ?, ?,

                        ?, ?, ?, ?,

                        ?, ?, ?, ?,

                        ?, ?, ?, ?

                    )
                    """,
                    (
                        entity_id,
                        entity_name,
                        clean_csv_value(
                            row.get("Description", "")
                        ),
                        data_domain,
                        data_classification,

                        owner_division_head,
                        owner_division,
                        owner_department_head,
                        owner_department,

                        clean_csv_value(
                            row.get(
                                "Data Steward 1 - Division Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 1 Division",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 1 - Department Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 1 Department",
                                ""
                            )
                        ),

                        clean_csv_value(
                            row.get(
                                "Data Steward 2 - Division Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 2 Division",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 2 - Department Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 2 Department",
                                ""
                            )
                        ),

                        clean_csv_value(
                            row.get(
                                "Data Steward 3 - Division Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 3 Division",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 3 - Department Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Steward 3 Department",
                                ""
                            )
                        ),

                        clean_csv_value(
                            row.get(
                                "Data Custodian 1 - Division Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 1 Division",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 1 - Department Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 1 Department",
                                ""
                            )
                        ),

                        clean_csv_value(
                            row.get(
                                "Data Custodian 2 - Division Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 2 Division",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 2 - Department Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 2 Department",
                                ""
                            )
                        ),

                        clean_csv_value(
                            row.get(
                                "Data Custodian 3 - Division Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 3 Division",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 3 - Department Head",
                                ""
                            )
                        ),
                        clean_csv_value(
                            row.get(
                                "Data Custodian 3 Department",
                                ""
                            )
                        )
                    )
                )

                processed_entities.add(
                    entity_id
                )

                imported_entities += 1


            # ------------------------------------------------
            # Save ownership assignment.
            #
            # Ownership Scope is intentionally NOT checked
            # for duplicates.
            # ------------------------------------------------

            cursor.execute(
                """
                INSERT INTO ownership_assignments (

                    entity_id,
                    ownership_scope,
                    program,
                    data_owner_division_head,
                    data_owner_division,
                    data_owner_department_head,
                    data_owner_department

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entity_id,
                    ownership_scope,

                    clean_csv_value(
                        row.get("Program", "")
                    ),

                    owner_division_head,
                    owner_division,
                    owner_department_head,
                    owner_department
                )
            )

            imported_assignments += 1


        connection.commit()

        return {
            "success": len(errors) == 0,
            "imported_entities": imported_entities,
            "imported_assignments": imported_assignments,
            "skipped_rows": skipped_rows,
            "errors": errors
        }


    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "imported_entities": 0,
            "imported_assignments": 0,
            "skipped_rows": skipped_rows,
            "errors": [
                str(error)
            ]
        }

    finally:

        connection.close()


# ============================================================
# CDE REGISTRY
# ============================================================

def save_cde(
    cde_reference_id,
    cde,
    attribute,
    description,
    data_domain_entity,
    system_of_record,
    data_classification,
    lifecycle_stage,
    date_created,
    date_updated,
    retention_period,
    scheduled_archival_date,
    actual_archival_date,
    scheduled_deletion_date,
    actual_deletion_date
):
    """
    Create a new CDE record.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO cde_registry (

            cde_reference_id,
            cde,
            attribute,
            description,
            data_domain_entity,
            system_of_record,
            data_classification,
            lifecycle_stage,
            date_created,
            date_updated,
            retention_period,
            scheduled_archival_date,
            actual_archival_date,
            scheduled_deletion_date,
            actual_deletion_date

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            cde_reference_id,
            cde,
            attribute,
            description,
            data_domain_entity,
            system_of_record,
            data_classification,
            lifecycle_stage,
            date_created,
            date_updated,
            retention_period,
            scheduled_archival_date,
            actual_archival_date,
            scheduled_deletion_date,
            actual_deletion_date
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# GET CDE REGISTRY
# ============================================================

def get_cde_registry():

    connection = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT

            id,
            cde_reference_id,
            cde,
            attribute,
            description,
            data_domain_entity,
            system_of_record,
            data_classification,
            lifecycle_stage,
            date_created,
            date_updated,
            retention_period,
            scheduled_archival_date,
            actual_archival_date,
            scheduled_deletion_date,
            actual_deletion_date

        FROM cde_registry

        ORDER BY id
        """,
        connection
    )

    connection.close()

    return dataframe


# ============================================================
# UPDATE CDE
# ============================================================

def update_cde(
    cde_id,
    cde_reference_id,
    cde,
    attribute,
    description,
    data_domain_entity,
    system_of_record,
    data_classification,
    lifecycle_stage,
    date_created,
    date_updated,
    retention_period,
    scheduled_archival_date,
    actual_archival_date,
    scheduled_deletion_date,
    actual_deletion_date
):
    """
    Update an existing CDE record using its database ID.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE cde_registry

        SET

            cde_reference_id = ?,
            cde = ?,
            attribute = ?,
            description = ?,
            data_domain_entity = ?,
            system_of_record = ?,
            data_classification = ?,
            lifecycle_stage = ?,
            date_created = ?,
            date_updated = ?,
            retention_period = ?,
            scheduled_archival_date = ?,
            actual_archival_date = ?,
            scheduled_deletion_date = ?,
            actual_deletion_date = ?

        WHERE id = ?
        """,
        (
            cde_reference_id,
            cde,
            attribute,
            description,
            data_domain_entity,
            system_of_record,
            data_classification,
            lifecycle_stage,
            date_created,
            date_updated,
            retention_period,
            scheduled_archival_date,
            actual_archival_date,
            scheduled_deletion_date,
            actual_deletion_date,
            cde_id
        )
    )

    updated = cursor.rowcount > 0

    connection.commit()

    connection.close()

    return updated


# ============================================================
# DELETE CDE
# ============================================================

def delete_cde(cde_id):
    """
    Delete one CDE record using its database ID.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM cde_registry
        WHERE id = ?
        """,
        (cde_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()

    connection.close()

    return deleted
# ==========================================================
# SAVE CDE ASSESSMENT
# ==========================================================

def save_cde_assessment(

    assessment_date,
    data_element,
    attribute,
    description,
    data_domain_entity,
    system_of_record,
    data_classification,
    business_usage,
    critical_process,
    enterprise_usage,
    decision_making,
    management_reporting,
    regulatory_requirement,
    regulatory_reporting,
    financial_impact,
    risk_impact,
    customer_impact,
    data_quality_impact,
    enterprise_importance,
    assessment_notes,
    assessment_reviewer,
    assessment_score,
    recommendation,
    governance_decision,
    governance_rationale

):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO cde_assessments (

            assessment_date,

            data_element,
            attribute,
            description,
            data_domain_entity,
            system_of_record,
            data_classification,

            business_usage,
            critical_process,
            enterprise_usage,
            decision_making,
            management_reporting,

            regulatory_requirement,
            regulatory_reporting,
            financial_impact,
            risk_impact,
            customer_impact,
            data_quality_impact,
            enterprise_importance,

            assessment_notes,
            assessment_reviewer,

            assessment_score,
            recommendation,

            governance_decision,
            governance_rationale

        )

        VALUES (

            ?,

            ?,
            ?,
            ?,
            ?,
            ?,
            ?,

            ?,
            ?,
            ?,
            ?,
            ?,

            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,

            ?,
            ?,

            ?,
            ?,

            ?,
            ?

        )
        """,

        (

            assessment_date,

            data_element,
            attribute,
            description,
            data_domain_entity,
            system_of_record,
            data_classification,

            business_usage,
            critical_process,
            enterprise_usage,
            decision_making,
            management_reporting,

            regulatory_requirement,
            regulatory_reporting,
            financial_impact,
            risk_impact,
            customer_impact,
            data_quality_impact,
            enterprise_importance,

            assessment_notes,
            assessment_reviewer,

            assessment_score,
            recommendation,

            governance_decision,
            governance_rationale

        )

    )

    connection.commit()

    assessment_id = cursor.lastrowid

    connection.close()

    return assessment_id
