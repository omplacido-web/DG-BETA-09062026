# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

# Import sqlite3 so Python can communicate with
# our SQLite database.
import sqlite3


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

# This function creates a connection to our SQLite database.
def get_connection():

    # Connect to the governance.db database file.
    # SQLite will create the file if it does not exist.
    connection = sqlite3.connect("governance.db")

    # Return the database connection.
    return connection


# ==========================================================
# CREATE DATA OWNER REGISTRY TABLE
# ==========================================================

# This function creates the main Data Owner Registry
# table if it does not already exist.
def create_tables():

    # Open a connection to the database.
    connection = get_connection()

    # Create a cursor so we can execute SQL commands.
    cursor = connection.cursor()

    # Create the Data Owner Registry table.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS data_owner_registry (

            -- Internal database record number.
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Unique identifier for the data entity.
            entity_id TEXT NOT NULL,

            -- Business name of the data entity.
            entity_name TEXT NOT NULL,

            -- Description of the data entity.
            description TEXT,

            -- Data domain associated with the entity.
            data_domain TEXT,

            -- Legacy ownership scope field.
            ownership_scope TEXT,

            -- Data classification assigned to the entity.
            data_classification TEXT,


            -- =================================================
            -- DATA OWNER
            -- =================================================

            -- Data Owner at Division Head level.
            data_owner_division_head TEXT,

            -- Division of the Data Owner.
            data_owner_division TEXT,

            -- Data Owner at Department Head level.
            data_owner_department_head TEXT,

            -- Department of the Data Owner.
            data_owner_department TEXT,


            -- =================================================
            -- DATA STEWARD 1
            -- =================================================

            -- Data Steward 1 at Division Head level.
            data_steward_1_division_head TEXT,

            -- Division of Data Steward 1.
            data_steward_1_division TEXT,

            -- Data Steward 1 at Department Head level.
            data_steward_1_department_head TEXT,

            -- Department of Data Steward 1.
            data_steward_1_department TEXT,


            -- =================================================
            -- DATA STEWARD 2
            -- =================================================

            -- Data Steward 2 at Division Head level.
            data_steward_2_division_head TEXT,

            -- Division of Data Steward 2.
            data_steward_2_division TEXT,

            -- Data Steward 2 at Department Head level.
            data_steward_2_department_head TEXT,

            -- Department of Data Steward 2.
            data_steward_2_department TEXT,


            -- =================================================
            -- DATA STEWARD 3
            -- =================================================

            -- Data Steward 3 at Division Head level.
            data_steward_3_division_head TEXT,

            -- Division of Data Steward 3.
            data_steward_3_division TEXT,

            -- Data Steward 3 at Department Head level.
            data_steward_3_department_head TEXT,

            -- Department of Data Steward 3.
            data_steward_3_department TEXT,


            -- =================================================
            -- DATA CUSTODIAN 1
            -- =================================================

            -- Data Custodian 1 at Division Head level.
            data_custodian_1_division_head TEXT,

            -- Division of Data Custodian 1.
            data_custodian_1_division TEXT,

            -- Data Custodian 1 at Department Head level.
            data_custodian_1_department_head TEXT,

            -- Department of Data Custodian 1.
            data_custodian_1_department TEXT,


            -- =================================================
            -- DATA CUSTODIAN 2
            -- =================================================

            -- Data Custodian 2 at Division Head level.
            data_custodian_2_division_head TEXT,

            -- Division of Data Custodian 2.
            data_custodian_2_division TEXT,

            -- Data Custodian 2 at Department Head level.
            data_custodian_2_department_head TEXT,

            -- Department of Data Custodian 2.
            data_custodian_2_department TEXT,


            -- =================================================
            -- DATA CUSTODIAN 3
            -- =================================================

            -- Data Custodian 3 at Division Head level.
            data_custodian_3_division_head TEXT,

            -- Division of Data Custodian 3.
            data_custodian_3_division TEXT,

            -- Data Custodian 3 at Department Head level.
            data_custodian_3_department_head TEXT,

            -- Department of Data Custodian 3.
            data_custodian_3_department TEXT

        )
        """
    )

    # Save the table creation.
    connection.commit()

    # Close the database connection.
    connection.close()

    # Create the additional governance tables.
    add_ownership_scope_column()
    create_cde_table()
    create_ownership_assignments_table()
    create_cde_assessments_table()


# ==========================================================
# ADD OWNERSHIP SCOPE COLUMN
# ==========================================================

# This function checks whether the existing database
# already contains the ownership_scope column.
def add_ownership_scope_column():

    # Open the database connection.
    connection = get_connection()

    # Create a cursor for executing SQL commands.
    cursor = connection.cursor()

    # Ask SQLite for information about the columns
    # currently existing in the data_owner_registry table.
    cursor.execute(
        """
        PRAGMA table_info(data_owner_registry)
        """
    )

    # Retrieve all column information.
    columns = cursor.fetchall()

    # Create a list containing only the column names.
    column_names = [
        column[1]
        for column in columns
    ]

    # Check whether ownership_scope is missing.
    if "ownership_scope" not in column_names:

        # Add the missing ownership_scope column.
        cursor.execute(
            """
            ALTER TABLE data_owner_registry
            ADD COLUMN ownership_scope TEXT
            """
        )

        # Save the database change.
        connection.commit()

    # Close the database connection.
    connection.close()


# ==========================================================
# CREATE CDE TABLE
# ==========================================================

# This function creates the Critical Data Element
# registry table if it does not already exist.
#
# IMPORTANT:
# The existing governance.db may already contain a more
# advanced CDE registry structure.
#
# Because we use CREATE TABLE IF NOT EXISTS, SQLite will
# NOT replace or modify an existing cde_registry table.
def create_cde_table():

    # Open the database connection.
    connection = get_connection()

    # Create a cursor.
    cursor = connection.cursor()

    # Create the CDE registry table only if it does not exist.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cde_registry (

            cde_id INTEGER PRIMARY KEY AUTOINCREMENT,

            cde_name TEXT NOT NULL,

            description TEXT,

            entity_name TEXT,

            data_domain TEXT

        )
        """
    )

    # Save the change.
    connection.commit()

    # Close the database connection.
    connection.close()


# ==========================================================
# CREATE OWNERSHIP ASSIGNMENTS TABLE
# ==========================================================

# This function creates the Ownership Assignments table.
#
# One Data Entity can have multiple Data Owner assignments.
#
# Example:
#
# Customer Entity
#     |
#     +-- Retail Banking      -> Owner A
#     |
#     +-- Wealth Management   -> Owner B
#     |
#     +-- Corporate Banking   -> Owner C
#
# This is a one-to-many relationship:
#
# One Entity -> Many Ownership Assignments
def create_ownership_assignments_table():

    # Open the database connection.
    connection = get_connection()

    # Create a cursor.
    cursor = connection.cursor()

    # Create the ownership_assignments table.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ownership_assignments (

            -- Internal database record number.
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Entity ID connected to this assignment.
            entity_id TEXT NOT NULL,

            -- Business or organizational scope
            -- covered by this ownership assignment.
            ownership_scope TEXT NOT NULL,

            -- Program associated with the assignment.
            program TEXT,

            -- Data Owner at Division Head level.
            data_owner_division_head TEXT,

            -- Division of the Data Owner.
            data_owner_division TEXT,

            -- Data Owner at Department Head level.
            data_owner_department_head TEXT,

            -- Department of the Data Owner.
            data_owner_department TEXT

        )
        """
    )

    # Save the table creation.
    connection.commit()

    # Close the database connection.
    connection.close()


# ==========================================================
# CREATE CDE ASSESSMENTS TABLE
# ==========================================================

# This table stores the history of CDE Identification
# assessments.
#
# It is separate from cde_registry because an assessment
# is NOT automatically a confirmed CDE.
#
# This allows us to preserve:
#
# - What was assessed
# - How it was assessed
# - The score
# - The recommendation
# - The governance decision
# - The governance rationale
# - Who performed the assessment
def create_cde_assessments_table():

    # Open the database connection.
    connection = get_connection()

    # Create a cursor.
    cursor = connection.cursor()

    # Create the CDE assessment history table.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cde_assessments (

            -- Internal assessment record number.
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Date and time when the assessment was created.
            assessment_date TEXT NOT NULL,

            -- Candidate Critical Data Element name.
            data_element TEXT NOT NULL,

            -- Attribute or physical/logical field name.
            attribute TEXT NOT NULL,

            -- Business description of the data element.
            description TEXT,

            -- Data domain or entity.
            data_domain_entity TEXT,

            -- System of Record.
            system_of_record TEXT,

            -- Data classification.
            data_classification TEXT,


            -- =================================================
            -- BUSINESS CONTEXT
            -- =================================================

            -- Description of business usage.
            business_usage TEXT,

            -- Whether the element is used in a critical process.
            critical_process TEXT,

            -- Whether the element is used across the enterprise.
            enterprise_usage TEXT,

            -- Whether the element supports important decisions.
            decision_making TEXT,

            -- Whether the element is used in management reporting.
            management_reporting TEXT,


            -- =================================================
            -- CDE ASSESSMENT CRITERIA
            -- =================================================

            -- Required by law or regulation.
            regulatory_requirement TEXT,

            -- Used in regulatory reporting.
            regulatory_reporting TEXT,

            -- Financial impact.
            financial_impact TEXT,

            -- Risk and compliance impact.
            risk_impact TEXT,

            -- Customer impact.
            customer_impact TEXT,

            -- Data quality impact.
            data_quality_impact TEXT,

            -- Enterprise importance.
            enterprise_importance TEXT,


            -- =================================================
            -- ASSESSMENT DETAILS
            -- =================================================

            -- Additional notes from the assessor.
            assessment_notes TEXT,

            -- Person who performed the assessment.
            assessment_reviewer TEXT,


            -- =================================================
            -- ASSESSMENT RESULT
            -- =================================================

            -- Calculated assessment score.
            assessment_score INTEGER,

            -- System-generated recommendation.
            recommendation TEXT,


            -- =================================================
            -- GOVERNANCE DECISION
            -- =================================================

            -- Final governance decision.
            governance_decision TEXT,

            -- Explanation supporting the governance decision.
            governance_rationale TEXT

        )
        """
    )

    # Save the table creation.
    connection.commit()

    # Close the database connection.
    connection.close()