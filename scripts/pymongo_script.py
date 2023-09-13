from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ayushmaanFCB:ayonmongodb@cluster0.2uzsu2q.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["NER_from_Documents_Project"]
collection = db["Resumes"]

post = {
    "_id": 0,
    "basics": {
        "name": [
            "Rahul Punjani"
        ],
        "email": [
            "Rahul_punjani@yahoo.com"
        ],
        "phone": [
            "+91-7977016370"
        ],
        "url": [],
        "location": [
            "Hinjewadi",
            "Pune"
        ],
        "language": [
            "English",
            "Hindi",
            "Marathi"
        ]
    },
    "academics": {
        "course": [],
        "education": [
            "college Malad, Mumbai",
            "Higher Secondary (Science) \u2013 2012.Saraf college Malad, Mumbai"
        ]
    },
    "work": {
        "company": [
            "Wipro Ltd..",
            "Infosys Ltd.."
        ],
        "position": [
            "Java Developer since October 2019 till date",
            "Java Developer",
            "System Engineer"
        ],
        "experience": [
            "five plus years in IT industry",
            "Experience of Java coding and unit testing",
            "Experience in configuration of customer service network"
        ]
    },
    "expertise": {
        "skill": [
            ".PROG",
            "LANGUAGE.Java",
            "SQL.FRAMEWORK.Spring",
            "MVC",
            "Spring Boot",
            "Microservice",
            "Hibernate",
            "Junit",
            "Mockito",
            "Postman",
            "MYSQL",
            "PostgreSQL.IDE.Eclipse",
            "IntelliJ Idea",
            "STS",
            "TOOL.Maven",
            "Linux",
            "WEB TECHNOLOGY.HTML",
            "CSS.TOOLS.Git",
            "SVN",
            "Jenkins",
            "Jira",
            "CLOUD.AWS",
            "EC2",
            "Lambda",
            "SNS",
            "Java",
            "Spring boot",
            "Hibernate",
            "Eclipse",
            "Junit",
            "SVN",
            "Hudson",
            "Oracle",
            "Java",
            "Spring MVC",
            "Eclipse",
            "Junit",
            "Git",
            "Java",
            "Spring",
            "Hibernate",
            "HTML",
            "Eclipse",
            "Junit",
            "Mockito",
            "Git",
            "Jenkins",
            "Oracle",
            "Gujrati"
        ],
        "project": [
            "Canadian Mortgage Technology (May 2019 \u2013 Sept 2019)",
            "Expert is the industry leading solution.having",
            "Century Link, Aug 2016 \u2013 April 2019",
            "Century Link",
            "HOBBIES.\t\tTravelling.\t\tCooking"
        ]
    },
    "achievements": {
        "certification": [
            "Certificate of Appreciation for delivering quality with handling highest number of services without any Human Error Outage..Awarded Best"
        ],
        "award": [
            "Best Debutant award for exceptionally individual performance in May 2017"
        ],
        "publication": []
    }
}


try:
    collection.insert_one(post)
except Exception as e:
    print(e)
