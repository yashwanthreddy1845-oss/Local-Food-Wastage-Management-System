USE food_wastage;

-- 1. Total Food Available

SELECT SUM(Quantity) AS Total_Food_Available
FROM food_listings;


-- 2. Food Listings by Location

SELECT Location,
       COUNT(*) AS Total_Listings
FROM food_listings
GROUP BY Location
ORDER BY Total_Listings DESC;


-- 3. Food Type Distribution

SELECT Food_Type,
       COUNT(*) AS Count_Food
FROM food_listings
GROUP BY Food_Type
ORDER BY Count_Food DESC;


-- 4. Provider Type Contribution

SELECT Provider_Type,
       SUM(Quantity) AS Total_Food
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Food DESC;


-- 5. Providers by City

SELECT City,
       COUNT(*) AS Total_Providers
FROM providers
GROUP BY City
ORDER BY Total_Providers DESC;


-- 6. Receivers by City

SELECT City,
       COUNT(*) AS Total_Receivers
FROM receivers
GROUP BY City
ORDER BY Total_Receivers DESC;


-- 7. Providers List

SELECT Name,
       Contact,
       City
FROM providers
ORDER BY City;


-- 8. Top Receivers by Claims

SELECT r.Receiver_ID,
       r.Name,
       COUNT(c.Claim_ID) AS Total_Claims
FROM receivers r
JOIN claims c
ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY Total_Claims DESC;


-- 9. Most Claimed Food Items

SELECT Food_ID,
       COUNT(*) AS Total_Claims
FROM claims
GROUP BY Food_ID
ORDER BY Total_Claims DESC;


-- 10. Providers with Successful Claims

SELECT p.Provider_ID,
       p.Name,
       COUNT(c.Claim_ID) AS Successful_Claims
FROM providers p
JOIN food_listings f
ON p.Provider_ID = f.Provider_ID
JOIN claims c
ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID, p.Name
ORDER BY Successful_Claims DESC;


-- 11. Average Food Quantity

SELECT AVG(Quantity) AS Avg_Quantity
FROM food_listings;


-- 12. Meal Type Distribution

SELECT Meal_Type,
       COUNT(*) AS Total_Count
FROM food_listings
GROUP BY Meal_Type
ORDER BY Total_Count DESC;


-- 13. Top Providers by Food Donation

SELECT Provider_ID,
       SUM(Quantity) AS Total_Donated
FROM food_listings
GROUP BY Provider_ID
ORDER BY Total_Donated DESC;


-- 14. Top 10 Locations by Food Quantity

SELECT Location,
       SUM(Quantity) AS Total_Food
FROM food_listings
GROUP BY Location
ORDER BY Total_Food DESC
LIMIT 10;


-- 15. Provider Type Performance

SELECT Provider_Type,
       COUNT(*) AS Total_Listings,
       SUM(Quantity) AS Total_Food
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Food DESC;