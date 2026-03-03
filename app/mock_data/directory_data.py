# REAL: Replace with LDAP / Corporate Directory Service lookup

import random as _random

_random.seed(42)  # Deterministic for consistent mock data

_FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Emily", "Paul", "Donna", "Andrew", "Michelle", "Joshua", "Carol",
    "Kenneth", "Amanda", "Kevin", "Dorothy", "Brian", "Melissa", "George", "Deborah",
    "Timothy", "Stephanie", "Ronald", "Rebecca", "Edward", "Sharon", "Jason", "Laura",
    "Jeffrey", "Cynthia", "Ryan", "Kathleen", "Jacob", "Amy", "Gary", "Angela",
    "Nicholas", "Shirley", "Eric", "Anna", "Jonathan", "Brenda", "Stephen", "Pamela",
    "Larry", "Emma", "Justin", "Nicole", "Scott", "Helen", "Brandon", "Samantha",
    "Benjamin", "Katherine", "Samuel", "Christine", "Gregory", "Debra", "Alexander", "Rachel",
    "Patrick", "Carolyn", "Frank", "Janet", "Raymond", "Catherine", "Jack", "Maria",
    "Dennis", "Heather", "Jerry", "Diane", "Tyler", "Ruth", "Aaron", "Julie",
    "Jose", "Olivia", "Nathan", "Joyce", "Henry", "Virginia", "Peter", "Victoria",
    "Adam", "Kelly", "Zachary", "Lauren", "Douglas", "Christina", "Harold", "Joan",
    "Carl", "Evelyn", "Arthur", "Judith", "Roger", "Megan", "Ryan", "Andrea",
    "Albert", "Cheryl", "Lawrence", "Hannah", "Jesse", "Jacqueline", "Dylan", "Martha",
    "Bryan", "Gloria", "Joe", "Teresa", "Jordan", "Ann", "Billy", "Sara",
    "Bruce", "Madison", "Ralph", "Frances", "Roy", "Kathryn", "Eugene", "Janice",
    "Randy", "Jean", "Wayne", "Abigail", "Vincent", "Alice", "Philip", "Judy",
]

_LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales",
    "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
    "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward",
    "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray",
    "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel",
    "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell",
]

_DEPARTMENTS = [
    "Technology", "Engineering", "Platform Engineering", "Site Reliability",
    "Cloud Infrastructure", "Data Engineering", "Security Engineering",
    "Application Development", "DevOps", "Quality Engineering",
    "Product Management", "Infrastructure", "Network Engineering",
]

_TITLES = [
    "Software Engineer", "Senior Software Engineer", "Staff Engineer",
    "Site Reliability Engineer", "Senior SRE", "Platform Engineer",
    "DevOps Engineer", "Engineering Manager", "Technical Lead",
    "Application Developer", "Senior Developer", "Cloud Engineer",
    "Data Engineer", "Security Engineer", "QA Engineer",
    "Product Manager", "Senior Product Manager", "Scrum Master",
    "Principal Engineer", "Solutions Architect",
]

_SID_PREFIXES = "JABCDEFGHKLMNPRSTUVWX"


def _build_directory():
    people = []
    used_names = set()
    for i in range(200):
        while True:
            first = _random.choice(_FIRST_NAMES)
            last = _random.choice(_LAST_NAMES)
            if (first, last) not in used_names:
                used_names.add((first, last))
                break
        prefix = _SID_PREFIXES[i % len(_SID_PREFIXES)]
        sid = f"{prefix}{10000 + i}"
        email = f"{first.lower()}.{last.lower()}@jpmchase.com"
        dept = _random.choice(_DEPARTMENTS)
        title = _random.choice(_TITLES)
        people.append({
            "sid": sid,
            "firstName": first,
            "lastName": last,
            "email": email,
            "department": dept,
            "title": title,
        })
    return people


DIRECTORY = _build_directory()
