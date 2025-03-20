from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aws_secret import fetch_secret
from orm_class import Organization, Workflow, Intent, PreviewWorkflowUrl
print("-")
# PS_db_con_5.2 - PS_db_con_5.13 invoke the fetch_secret get the credential make the database connection and return the connection.
def db_connection():
    try:
        # PS_db_con_5.4 - SQ_DB_CON_5.2: Request database credentials
        db_secrets = fetch_secret('db_secrets')
        # # Construct the DATABASE_URI using fetched secrets
        DATABASE_URI = f"postgresql://{db_secrets['DB_USER']}:{db_secrets['DB_PASSWORD']}@" \
                       f"{db_secrets['DB_HOST']}:{db_secrets['DB_PORT']}/{'postgres'}"

        print(DATABASE_URI)
        # PS_db_con_5.6 - SQ_DB_CON_5.4: Initialize SQLAlchemy engine
        engine = create_engine(DATABASE_URI)

        # PS_db_con_5.7 - SQ_DB_CON_5.5: Create sessionmaker
        SessionLocal = sessionmaker(bind=engine)

        # PS_db_con_5.8 - SQ_DB_CON_5.6: Instantiate a new database session
        db_session = SessionLocal()
        print(db_session)

        # PS_db_con_5.9 - SQ_DB_CON_5.7: Return the database session
      
        return db_session

    except Exception as e:
        print("Error from db_connection",e)
        raise str(e)
    
from orm_class import Organization

def check_db_for_org(organization_name):
    try:
        # Implement your database query logic here
        session = db_connection()
        result = session.query(Organization.organization_id).filter_by(organization_name=organization_name).first()
        if result:
            print(f"Organization found: {result}")
            return result.organization_id
        return False
    except Exception as e:
        print(f"Error in check_db_for_org: {str(e)}")
        raise e
        
def get_workflows_by_organization_name(organization_id):
    try:
        print(organization_id,"......")
        session = db_connection()
        workflows = (
            session.query(Workflow.workflow_id)
            .select_from(Organization)
            .join(Workflow, Workflow.organization_id == Organization.organization_id)
            .filter(Organization.organization_id == organization_id)
            .all()
        )
        return [workflow.workflow_id for workflow in workflows]
    except Exception as e:
        print(f"Error in get_workflows_by_organization_name: {str(e)}")
        raise e

def get_all_intent_names_by_workflow_id(workflow_id):
    try:
        session = db_connection()
        intents = session.query(Intent.intent_name).filter_by(workflow_id=workflow_id).all()
        return [intent.intent_name for intent in intents]
    except Exception as e:
        print(f"Error in get_all_intent_names_by_workflow_id: {str(e)}")
        raise e

def get_all_intents_by_organization_name(organization_id):
    try:
        workflows = get_workflows_by_organization_name(organization_id)
        all_intents = []
        for workflow_id in workflows:
            intents = get_all_intent_names_by_workflow_id(workflow_id)
            all_intents.extend(intents)
        return all_intents
    except Exception as e:
        print(f"Error in get_all_intents_by_organization_name: {str(e)}")
        raise e
    
def check_db_for_workflow(intent_name, organization_id):
    # Step 1: Check if the intent exists and get the workflow_id
    try:
        session = db_connection()
        intent = session.query(Intent).filter_by(intent_name=intent_name).first()
        if intent:
            workflow_id = intent.workflow_id
            print(f"Workflow ID found: {workflow_id}")
            print(f"Organization ID: {organization_id}")
           
            # Step 2: Get the deployed_url based on the workflow_id and organization_id
            preview_workflow = session.query(PreviewWorkflowUrl).filter_by(
                workflow_id=workflow_id,
                organization_id=organization_id
            ).first()
           
            if preview_workflow:
                return preview_workflow.deployed_url
       
        return False
    except Exception as e:
        print(f"Error in check_db_for_workflow: {str(e)}")
        raise e
