query1 = ("SELECT signup_date, COUNT(*) AS user_count FROM users "
            " GROUP BY signup_date "
            " ORDER BY signup_date DESC; ")

query2 = "SELECT DISTINCT domain FROM users;"

query3 = ("SELECT * FROM users"
            " WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days';")

query4 = ("WITH DomainCount AS ("
                "SELECT domain, COUNT(*) AS domain_count FROM users"
                " GROUP BY domain"
                " ORDER BY domain_count DESC"
                " LIMIT 1 )"
            " SELECT u.name, u.email, u.domain FROM users u"
            " JOIN DomainCount dc ON u.domain = dc.domain;")

query5 = ("DELETE FROM users"
            " WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'example.com');")