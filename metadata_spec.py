#%%

from typing import Optional, List 
from pydantic.errors import SetMaxLengthError
from sqlalchemy import engine
from sqlalchemy.sql.expression import table
from typing import Optional, Literal
from sqlmodel import Field, SQLModel, create_engine
from datetime import date, datetime

class Sample(SQLModel, table=True):
    # biobank sample id
    sample_id: str = Field(primary_key=True)

    individual_id: str
    sampling_time: datetime
    specimen_tissue_source: str
    anatomical_source: str
    storage_type: str
    specimen_type: str
    # sql model doesn't support this yest "Literal['tumor', 'normal']" 
    tumor_normal_designation: str
    tumor_state: str
    # time interval thus 
    time_to_storage: float
    # # time interval and optional 
    fixation_time: Optional[float] = None
    # should be but not supported Literal["yea", "no", "na"]
    treatment_before_sampling: str
    treatment_before_sampling_details: Optional[str] = None
    histological_diagnosis_icd10: str
    histological_diagnosis_icdo3: str
    tumor_purity_he: float

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    ican_patient_id: str
    sample_id: Optional[str] = Field(default=None, foreign_key='sample.sample_id')

   
class Organoids(SQLModel, table=True):
    # This id will be set by database no need to validate
    id: Optional[int] = Field(default=None, primary_key=True)

    anatomical_source: str
    treatment_before_sampling: str
    organoid_prep_start: datetime
    days_of_culture: float
    days_since_passage: Optional[float] = None
    cell_content_prep_start: datetime
    organoid_treatment: str
    
    
    sample_id: Optional[int] = Field(default=None, foreign_key="sample.sample_id")


class Study(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    principal_investigator: str
    pi_contact: str
    submitter: str
    submitter_contact: str
    study_info: str

    sample_id: Optional[int] = Field(default=None, foreign_key="sample.sample_id")

class Sequencing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    seq_coverage: int
    number_of_reads: int
    cell_selections: str
    target_of_sequencing: str
    nucleid_acid_isolation: str
    barcoding: str
    pcr_free: bool
    target_enrichment: str
    probe_manufacturer: str
    target_enrichment_batch: str
    umi: bool
    insert_size: int
    rna_integrity: int
    rnaseq_dna_contamination: str
    sample_prep_start: datetime
    sample_prep_end: datetime
    input_amount: float
    nucleid_acid_concentration: float
    sequencing_date: datetime
    sequencing_platform: str
    sequencing_instrument: str
    flowcell_type: str
    paired_end: bool
    read_length: int
    sequencing_batch: str
    pre_seq_qpcr: str

    sample_id: Optional[int] = Field(default=None, foreign_key="sample.sample_id")

class Ex_Vivo_Drug_Screening(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    experiment_date: datetime
    experiment_type: str
    medium: str
    incubation_time: datetime
    plate: str
    # path to file
    plateset_file: str
    # path to file
    sop_file: str 
    cell_of_origin: str
    cell_type: str
    readout_type: str
    reader: str
    # path to file
    reader_results_file: str

    sample_id: Optional[int] = Field(default=None, foreign_key="sample.sample_id")

class Imaging_Common(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    modality: str
    instrument: str
    instrument_id: str
    dataset_dims: float
    spatial_dims: float
    timestamps: datetime
    data_type: str

    sample_id: Optional[int] = Field(default=None, foreign_key="sample.sample_id")


class Imaging_Microscopy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    stain_names:  List[str]
    assay_name: str
    objective_magnification: str
    objective_na: float
    no_of_channels: float
    excitation_wavelengths: List[float]
    emission_wavelengths: float
    excitation_time: Optional[List[float]] = None
    excitation_power: Optional[List[float]] = None
    overlap: Optional[float] = None
    holder_type: str
    holder_id: str
    holder_batch: str
    dataset_id: str
    dataset_folder: str
    dataset_annotations: str
    dataset_acquisition_datetime: datetime
    # should be of type complex but not supported
    dataset_pixels: str
    dataset_channels: str

    image_id: Optional[int] = Field(default=None, foreign_key="imaging_common.id")

# define the databse url

## sqlite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

## mysql
mysql_file_name = ""
mysql_url = f""

## 

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)
# %%
