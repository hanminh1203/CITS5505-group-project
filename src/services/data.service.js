class DataService {
    requests = [
        {
            id: 1234,
            owner: {
                id: 5123,
                name: 'John Doe',
                address: 'Perth, AU',
                bio: 'Full-stack developer & photography enthusiast. Member since Jan 2025.'

            },
            offering: {
                skills: [
                    {
                        name: 'Guitar',
                        category: {
                            name: 'Music'
                        }
                    },
                    {
                        name: 'Piano',
                        category: {
                            name: 'Music'
                        }
                    },
                    {
                        name: 'Violin',
                        category: {
                            name: 'Music'
                        }
                    }
                ],
                message: 'I can teach Python from beginner to advanced, data science workflows, web scraping, or API development. Happy to customize based on what you want to learn.'
            },
            skill: {
                name: 'Guitar',
                category: {
                    name: 'Music'
                }
            },
            description: `I'm a backend developer with 4 years of experience in Python and Django. I'm looking to expand my frontend skills and learn React and Next.js properly — not just tutorials, but building real projects.
            I'm hoping for weekly sessions (1-2 hours each) over 2-3 months. I prefer video calls via Google Meet or Zoom. My timezone is AEDT (UTC+11).
            I'll tailor our sessions around your teaching style. I'm a fast learner and I'm comfortable with JavaScript fundamentals already.`,
            level: 'BEGINNER',
            status: 'OPEN',
            format: 'Online',
            duration: '1-2 hours per week',
            availability: 'Weekday evenings (AEDT)',
            offers: [
                {
                    id: 1234,
                    offerer: {
                        user: {
                            name: 'John Doe II'
                        },
                        level: 'BEGINNER',
                        skill: {
                            name: 'Drawing',
                            category: {
                                name: 'Art'
                            }
                        },
                        message: "Hi Alex! I've been building with React for 5 years and Next.js for 3. I'd love to do a structured 8-week curriculum. I'm keen to learn Python for my ML side projects."
                    }
                },
                {
                    id: 1234,
                    offerer: {
                        user: {
                            name: 'John Doe III'
                        },
                        level: 'BEGINNER',
                        skill: {
                            name: 'Running',
                            category: {
                                name: 'Sport'
                            }
                        },
                        message: "I'm a freelance dev specialising in Next.js. Happy to teach practical app-building from scratch. I'd love to improve my data analysis skills for client reporting."
                    }
                },
            ],
            createdAt: this.addDay(new Date(), -30)
        }
    ]

    constructor() {
        this.requests.forEach(request => {
            request.owner.initial = this.getInitials(request.owner.name);
            request.createdAtAsTime = this.formatDDMMYYYY(new Date(request.createdAt));
            request.offers.forEach((offer) => {
                const offerer = offer.offerer;
                offerer.user.initial = this.getInitials(offerer.user.name);
            });
        });
    }

    async findRequestById(id) {
        return this.requests.find(request => request.id === id);
    }

    getInitials(name) {
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

    formatDDMMYYYY(date) {
        const dd = String(date.getDate()).padStart(2, "0");
        const mm = String(date.getMonth() + 1).padStart(2, "0"); // months are 0-based
        const yyyy = date.getFullYear();
        return `${dd}/${mm}/${yyyy}`;
    }
    addDay(date, days) {
        const newDate = new Date(date);
        newDate.setDate(newDate.getDate() + days);
        return newDate;
    }
}

export const service = new DataService();