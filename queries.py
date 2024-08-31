from sqlalchemy import text


query1 = text("SELECT signup_date, COUNT(*) AS user_count FROM users "            
            " GROUP BY signup_date "
            " ORDER BY signup_date DESC; ")

query2 = text("SELECT DISTINCT domain FROM users;")

query3 = text("SELECT * FROM users"
            " WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days';")

query4 = text("WITH DomainCount AS ("
                "SELECT domain, COUNT(*) AS domain_count FROM users"
                " GROUP BY domain"
                " ORDER BY domain_count DESC"
                " LIMIT 1 )"
            " SELECT u.name, u.email, u.domain FROM users u"
            " JOIN DomainCount dc ON u.domain = dc.domain;")

query5 = text("DELETE FROM users"
            " WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'example.com');")