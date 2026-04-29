class SkillLevel {
    static BEGINNER = 'BEGINNER'
    static INTERMEDIATE = 'INTERMEDIATE'
    static ADVANCED = 'ADVANCED'
}
class DataService {
    users = [
        {
            id: 1,
            name: 'John Doe',
            address: 'Perth, AU',
            bio: 'Full-stack developer & photography enthusiast. Member since Jan 2005.'

        },
        {
            id: 2,
            name: 'John Doe II',
            address: 'Perth, AU',
            bio: 'Full-stack developer & photography enthusiast. Member since Jan 2015.'

        },
        {
            id: 3,
            name: 'John Doe III',
            address: 'Perth, AU',
            bio: 'Full-stack developer & photography enthusiast. Member since Jan 2025.'

        }
    ];
    skillCategories = [
        {
            name: 'Music',
        },
        {
            name: 'Programming'
        },
        {
            name: 'Sport'
        }
    ];
    skills = [
        {
            name: 'Guitar',
            category: this.#findObjectByName(this.skillCategories, 'Music')
        },
        {
            name: 'Piano',
            category: this.#findObjectByName(this.skillCategories, 'Music')
        },
        {
            name: 'Violin',
            category: this.#findObjectByName(this.skillCategories, 'Music')
        },
        {
            name: 'React',
            category: this.#findObjectByName(this.skillCategories, 'Programming')
        },
        {
            name: 'Next.js',
            category: this.#findObjectByName(this.skillCategories, 'Programming')
        },
        {
            name: 'Python',
            category: this.#findObjectByName(this.skillCategories, 'Programming')
        },
        {
            name: 'Drawing',
            category: this.#findObjectByName(this.skillCategories, 'Art')
        },
        {
            name: 'Running',
            category: this.#findObjectByName(this.skillCategories, 'Sport')
        }
    ];

    requests = [
        {
            id: 1234,
            name: 'Learn React & Next.js from scratch',
            owner: this.#findObjectById(this.users, 1),
            offering: {
                skills: this.#findObjectByNames(this.skills, ['Guitar', 'Piano', 'Violin']),
                message: 'I can teach Python from beginner to advanced, data science workflows, web scraping, or API development. Happy to customize based on what you want to learn.'
            },
            skill: this.#findObjectByName(this.skills, 'React'),
            description: `I'm a backend developer with 4 years of experience in Python and Django. I'm looking to expand my frontend skills and learn React and Next.js properly — not just tutorials, but building real projects.
            I'm hoping for weekly sessions (1-2 hours each) over 2-3 months. I prefer video calls via Google Meet or Zoom. My timezone is AEDT (UTC+11).
            I'll tailor our sessions around your teaching style. I'm a fast learner and I'm comfortable with JavaScript fundamentals already.`,
            level: SkillLevel.BEGINNER,
            status: 'OPEN',
            format: 'Online',
            duration: '1-2 hours per week',
            availability: 'Weekday evenings (AEDT)',
            offers: [
                {
                    id: 1234,
                    offerer: this.#findObjectById(this.users, 2),
                    level: SkillLevel.INTERMEDIATE,
                    skill: this.#findObjectByName(this.skills, 'Drawing'),
                    message: "Hi Alex! I've been building with React for 5 years and Next.js for 3. I'd love to do a structured 8-week curriculum. I'm keen to learn Python for my ML side projects."
                },
                {
                    id: 1234,
                    offerer: this.#findObjectById(this.users, 3),
                    level: SkillLevel.ADVANCED,
                    skill: this.#findObjectByName(this.skills, 'Running'),
                    message: "I'm a freelance dev specialising in Next.js. Happy to teach practical app-building from scratch. I'd love to improve my data analysis skills for client reporting."
                },
            ],
            createdAt: this.#addDay(new Date(), -30)
        }
    ]

    currentUser = this.#findObjectById(this.users, 1);

    constructor() {
        this.requests.forEach(request => {
            request.owner.initial = this.#getInitials(request.owner.name);
            request.createdAtAsTime = this.#formatDDMMYYYY(new Date(request.createdAt));
            request.offers.forEach((offer) => {
                const offerer = offer.offerer;
                offerer.initial = this.#getInitials(offerer.name);
            });
        });
    }

    async findRequestById(id) {
        return this.requests.find(request => request.id === id);
    }

    #getInitials(name) {
        if (!name) return "";
        return name
            .trim()
            .split(/\s+/)              // split by one or more spaces
            .filter(Boolean)           // remove empty parts
            .slice(0, 2)
            .map(part => part[0])      // first character of each word
            .join("")
            .toUpperCase();
    }

    #formatDDMMYYYY(date) {
        const dd = String(date.getDate()).padStart(2, "0");
        const mm = String(date.getMonth() + 1).padStart(2, "0"); // months are 0-based
        const yyyy = date.getFullYear();
        return `${dd}/${mm}/${yyyy}`;
    }
    #addDay(date, days) {
        const newDate = new Date(date);
        newDate.setDate(newDate.getDate() + days);
        return newDate;
    }

    #fetchData(obj, path) {
        if (path.length === 0 || typeof (obj) !== typeof ({})) {
            return obj;
        }
        const [field, ...rest] = path;
        return this.#fetchData(obj[field], rest);
    }

    fillDataValue(elementHtml, obj) {
        const element = $(elementHtml);
        element.find('[app-data-value]').get().forEach(element => {
            const value = this.#fetchData(obj, $(element).attr('app-data-value').split('.'));
            $(element).text(value);
        });
        element.find('[app-attr-value]').get().forEach(childElement => {
            const appAttrValue = $(childElement).attr('app-attr-value').split(',');
            appAttrValue.forEach(attrName => {
                $(childElement).attr(attrName, this.#format($(childElement).attr(attrName), obj));
            });
        })
        return element;
    }

    #format(template, data) {
        return template.replace(/{{([^}]+)}}/g, (match, key) => {
            return this.#fetchData(data, key.split('.'));
        });
    }

    #findObjectByName(lst, name) {
        return lst.find(obj => obj.name === name);
    }

    #findObjectById(lst, id) {
        return lst.find(obj => obj.id === id);
    }

    #findObjectByNames(lst, names) {
        return lst.filter(obj => names.includes(obj.name));
    }
}

export const service = new DataService();