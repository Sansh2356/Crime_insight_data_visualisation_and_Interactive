CREATE OR REPLACE PACKAGE autotheft_package AS
  -- Procedure to insert a new record
  PROCEDURE insert_autotheft_record(
    p_index_at        NUMBER,
    p_state           VARCHAR2,
    p_zone            VARCHAR2,
    p_autotheft_stolen NUMBER,
    p_year            NUMBER
  );

  -- Procedure to update an existing record
  PROCEDURE update_autotheft_record(
    p_index_at        NUMBER,
    p_state           VARCHAR2,
    p_zone            VARCHAR2,
    p_autotheft_stolen NUMBER,
    p_year            NUMBER
  );

  -- Procedure to delete a record by index
  PROCEDURE delete_autotheft_record(
    p_index_at NUMBER
  );

  -- Function to retrieve autotheft data by index
  FUNCTION get_autotheft_data(
    p_index_at NUMBER
  ) RETURN SYS_REFCURSOR;

END autotheft_package;
/

CREATE OR REPLACE PACKAGE BODY autotheft_package AS

  PROCEDURE insert_autotheft_record(
    p_index_at        NUMBER,
    p_state           VARCHAR2,
    p_zone            VARCHAR2,
    p_autotheft_stolen NUMBER,
    p_year            NUMBER
  ) IS
  BEGIN
    INSERT INTO autotheft_data (index_at, state, zone, autotheft_stolen, year)
    VALUES (p_index_at, p_state, p_zone, p_autotheft_stolen, p_year);
  END insert_autotheft_record;

  PROCEDURE update_autotheft_record(
    p_index_at        NUMBER,
    p_state           VARCHAR2,
    p_zone            VARCHAR2,
    p_autotheft_stolen NUMBER,
    p_year            NUMBER
  ) IS
  BEGIN
    UPDATE autotheft_data
    SET state = p_state,
        zone = p_zone,
        autotheft_stolen = p_autotheft_stolen,
        year = p_year
    WHERE index_at = p_index_at;
  END update_autotheft_record;

  PROCEDURE delete_autotheft_record(
    p_index_at NUMBER
  ) IS
  BEGIN
    DELETE FROM autotheft_data WHERE index_at = p_index_at;
  END delete_autotheft_record;

  FUNCTION get_autotheft_data(
    p_index_at NUMBER
  ) RETURN SYS_REFCURSOR IS
    v_cursor SYS_REFCURSOR;
  BEGIN
    OPEN v_cursor FOR
      SELECT index_at, state, zone, autotheft_stolen, year
      FROM autotheft_data
      WHERE index_at = p_index_at;

    RETURN v_cursor;
  END get_autotheft_data;

END autotheft_package;
/
-- Example Usage:
DECLARE
  v_cursor SYS_REFCURSOR;
BEGIN
  autotheft_package.insert_autotheft_record(1, 'State1', 'ZoneA', 10, 2023);
  autotheft_package.update_autotheft_record(1, 'State1', 'ZoneA', 15, 2023);

  OPEN v_cursor FOR autotheft_package.get_autotheft_data(1);

  -- Fetch and display data
  -- (You can fetch the data from the cursor as needed)
  
  CLOSE v_cursor;

  autotheft_package.delete_autotheft_record(1);
END;
/


TRIGGER IMPLEMENTATION :=

CREATE OR REPLACE TRIGGER autotheft_audit_trigger
BEFORE INSERT OR UPDATE OR DELETE ON autotheft_data
FOR EACH ROW
DECLARE
  v_action VARCHAR2(10);
BEGIN
  IF INSERTING THEN
    v_action := 'INSERT';
  ELSIF UPDATING THEN
    v_action := 'UPDATE';
  ELSIF DELETING THEN
    v_action := 'DELETE';
  END IF;

  -- Inserting audit trail information into the audit_table
  INSERT INTO audit_table (
    table_name,
    action_type,
    timestamp,
    user_name,
    old_index_at,
    old_state,
    old_zone,
    old_autotheft_stolen,
    old_year,
    new_index_at,
    new_state,
    new_zone,
    new_autotheft_stolen,
    new_year
  ) VALUES (
    'autotheft_data',
    v_action,
    SYSTIMESTAMP,
    USER,
    :OLD.index_at,
    :OLD.state,
    :OLD.zone,
    :OLD.autotheft_stolen,
    :OLD.year,
    :NEW.index_at,
    :NEW.state,
    :NEW.zone,
    :NEW.autotheft_stolen,
    :NEW.year
  );
END autotheft_audit_trigger;
/
