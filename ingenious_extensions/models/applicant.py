from dataclasses import dataclass
from typing import List, Union
from pydantic import BaseModel, Field
import json
from ingenious.utils.model_utils import List_To_Csv, Listable_Object_To_Csv, Object_To_Yaml

class RootModel_Applicant(BaseModel):
    brand: str
    model: str
    year: int
    price: float

@dataclass
class ProfessionalExperience:
    title: str
    start_date: str
    end_date: str
    company_name: str
    city: str
    state: str
    responsibilities: List[str]
    key_achievements: List[str]

@dataclass
class Education:
    degree: str
    date: str
    institution: str
    city: str
    state: str

@dataclass
class Affiliation:
    name: str
    role: str = ""

@dataclass
class Skill:
    name: str

@dataclass
class ExecutiveProfile:
    name: str
    title: str
    summary: str
    areas_of_expertise: List[str]
    professional_experience: List[ProfessionalExperience]
    education: List[Education]
    affiliations: List[Affiliation]
    skills: List[Skill]

class RootModel(BaseModel):

    def load_from_json(json_data: str):
        data = json.loads(json_data)
        root_model = RootModel(**data)
        executive_profile = ExecutiveProfile(
            name="",
            title="Director of Information Technology",
            summary="Performance-driven and accomplished Director of Information Technology offering a unique combination of operations and management experience. Strong leader with demonstrated success in managing and providing leadership in a diverse technological environment. Creative, dependable and enthusiastic change agent with a proven track record in improving efficiencies and reducing costs. Visionary with superior longterm planning and project management experience. Proven ability to implement standards and procedures that improve business processes and functionality. Skilled coalition-builder with management practices that motivate and improve staff performance levels while forming a cohesive team. Innovative and customer-oriented to formulate strategies to address service delivery demands and resource capacity.",
            areas_of_expertise=[
                "Executive Leadership/Management",
                "Information Technology",
                "Project Management",
                "Networking",
                "Relationship Building",
                "Operations/Administration"
            ],
            professional_experience=[
                ProfessionalExperience(
                    title="Director of Information Technology",
                    start_date="05/2000",
                    end_date="01/2014",
                    company_name="Company Name",
                    city="City",
                    state="State",
                    responsibilities=[
                        "Provides leadership in directing, planning, managing, and implementing the information technology needs of the City of Greensboro.",
                        "Provided oversight and direction for the Application Services, GIS, Network Services and Public Safety IT divisions.",
                        "Establishes guidelines and programs for effective information technology management.",
                        "Facilitates and implements City-wide strategic policy for planning, development, and deployment of information technology."
                    ],
                    key_achievements=[
                        "Generated a savings of $400K per year with the implementation of VoIP",
                        "Partnered with NCDOT and GDOT to implement a City-wide fiber optic network infrastructure",
                        "Implemented on-line payments for parking tickets and utility bills. Received over 1 million in payments to date",
                        "Over the last five years, maintained a 95% customer satisfaction rating with 98% uptime in server and network environment",
                        "Implemented virtualized server environment and business continuity site with redundant SAN, servers and network infrastructure",
                        "Re-established the Technology Advisory Committee."
                    ]
                ),
                ProfessionalExperience(
                    title="Network Services Manager",
                    start_date="07/1998",
                    end_date="05/2000",
                    company_name="Company Name",
                    city="City",
                    state="State",
                    responsibilities=[
                        "Managed the Desktop Services Division, which included the Help Desk, local area network, server administration, training and leasing of computer technology.",
                        "Maintained and assisted with the support for enterprise-wide technology deployment.",
                        "Ensured that the customers' technology needs were addressed and resolved in an efficient and effective manner."
                    ],
                    key_achievements=[
                        "Championed the organizational strategic initiative to implement a client-server environment with Microsoft Exchange and leasing of all computer technology",
                        "Managed and directed the installation of 900+ workstations ahead of schedule and under budget",
                        "Managed and implemented a $2.8 million internal service charge back structure for Help Desk support and leasing of computer technology",
                        "Implemented a custom Helpdesk Request application, which includes a customer satisfaction survey after each closed call."
                    ]
                ),
                ProfessionalExperience(
                    title="Data Communications Analyst",
                    start_date="06/1989",
                    end_date="07/1998",
                    company_name="Company Name",
                    city="City",
                    state="State",
                    responsibilities=[
                        "Installed, maintained, configured and analyzed the data communication needs for the City of Greensboro.",
                        "Installed and configured modems, multiplexers, routers, control units and DEC and IBM terminals.",
                        "Analyzed system needs and configuration requirements to acquire the appropriate equipment.",
                        "Managed, maintained and resolved complex system problems with the IBM Mainframe, VAX systems, and servers."
                    ],
                    key_achievements=[
                        "Configured 450+ users on All-In-One",
                        "Project leader on upgrading IBM Mainframe to VSE/ESA",
                        "Developed operations manual for IBM Mainframe",
                        "Employee of the Year finalist 1996."
                    ]
                ),
                ProfessionalExperience(
                    title="Electronics Technician",
                    start_date="09/1986",
                    end_date="06/1989",
                    company_name="Company Name",
                    city="City",
                    state="State",
                    responsibilities=[
                        "Repaired, installed, configured and maintained PC's, servers, modems and other communication equipment.",
                        "Installed and designed network and data communication circuits.",
                        "Managed setup and installed communication equipment which included mid-range servers, communications equipment, VAX systems and PC's."
                    ],
                    key_achievements=[
                        "Designed and installed the wiring and communications infrastructure for student registration",
                        "Established redundant communication links to remote sites",
                        "Developed and planned the communications infrastructure for campus computer labs."
                    ]
                )
            ],
            education=[
                Education(
                    degree="Certified Chief Information Officer (CIO)",
                    date="November 2005",
                    institution="UNC-Chapel Hill",
                    city="City",
                    state="State"
                ),
                Education(
                    degree="B.S : Industrial Technology (Electronics)",
                    date="1986",
                    institution="North Carolina A&T State University",
                    city="City",
                    state="State"
                )
            ],
            affiliations=[
                Affiliation(name="North Carolina Local Government Information Systems Association (NCLGISA)"),
                Affiliation(name="SouthEast Association of Telecommunications Officers and Advisors (SEATOA)"),
                Affiliation(name="Public Technology Inc. (PTI)"),
                Affiliation(name="Greensboro Municipal Credit Union",
                            role="Previous Board Member (Chairman, Technology Committee)"),
                Affiliation(name="Welfare Reform and Liaison Project (WRLP)", role="Previous Board Member"),
                Affiliation(name="National Forum for Black Public Administrators (NFBPA), Triad Chapter",
                            role="Previous President")
            ],
            skills=[
                Skill(name="budget"),
                Skill(name="client-server"),
                Skill(name="customer satisfaction"),
                Skill(name="DEC"),
                Skill(name="directing"),
                Skill(name="direction"),
                Skill(name="GIS"),
                Skill(name="Government"),
                Skill(name="Help Desk support"),
                Skill(name="Help Desk"),
                Skill(name="IBM"),
                Skill(name="IBM Mainframe"),
                Skill(name="information technology"),
                Skill(name="local area network"),
                Skill(name="leadership"),
                Skill(name="managing"),
                Skill(name="Microsoft Exchange"),
                Skill(name="modems"),
                Skill(name="enterprise"),
                Skill(name="Network"),
                Skill(name="organizational"),
                Skill(name="PC's"),
                Skill(name="Project leader"),
                Skill(name="routers"),
                Skill(name="Safety"),
                Skill(name="SAN"),
                Skill(name="servers"),
                Skill(name="strategic"),
                Skill(name="upgrading"),
                Skill(name="VAX"),
                Skill(name="VoIP"),
                Skill(name="VSE"),
                Skill(name="wiring")
            ]
        )

        return root_model

    # def display_bike_sales_as_table(self):
    #     table_data: List[RootModel_BikeSale_Extended] = []
    #
    #     for store in self.stores:
    #         for sale in store.bike_sales:
    #             store_name = store.name
    #             location = store.location
    #             rec = RootModel_BikeSale_Extended(store_name=store_name, location=location, **sale.model_dump())
    #             table_data.append(rec)
    #
    #     ret = Listable_Object_To_Csv(table_data, RootModel_BikeSale_Extended)
    #     # Note always provide tabular data with a heading as this allows our datatables extension to render the data correctly
    #     return "## Sales\n" + ret