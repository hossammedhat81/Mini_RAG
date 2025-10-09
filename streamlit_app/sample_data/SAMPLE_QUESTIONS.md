# 🎯 Sample Questions for Testing SQL RAG System

## 📊 About the Data

Your system has 3 datasets with Egyptian e& telecom customer data:

1. **customers.csv** - 10 customers (Cairo, Alexandria, Giza, Mansoura, Tanta)
2. **transactions.csv** - 18 recharge transactions (50-200 EGP)
3. **calls.csv** - 18 call records (local & international)

---

## 🟢 BASIC QUESTIONS (Count & List)

### Customer Questions:
```
How many customers do we have?
Show me all customers
List all customer names
What cities do our customers live in?
Show customers from Cairo
How many customers are from Alexandria?
List all customer phone numbers
Show me customer emails
```

### Transaction Questions:
```
How many transactions do we have?
Show me all transactions
What is the total recharge amount?
List all transaction amounts
How many completed transactions?
Show transactions over 100 EGP
What are the transaction types available?
```

### Call Questions:
```
How many calls were made?
Show me all calls
List all call durations
How many local calls do we have?
How many international calls were made?
What is the total call cost?
Show calls longer than 100 minutes
```

---

## 🟡 INTERMEDIATE QUESTIONS (Filtering & Aggregation)

### Customer Analysis:
```
Show customers older than 30
List customers from Cairo or Alexandria
How many customers registered in February?
Show the youngest customer
Who is the oldest customer?
List customers aged between 25 and 35
Show customers registered after February 1st
Which cities have more than 2 customers?
```

### Transaction Analysis:
```
What is the average recharge amount?
Show transactions above average amount
List the top 5 largest transactions
What is the minimum recharge amount?
What is the maximum recharge amount?
Show transactions in February 2024
How much was recharged in March?
List transactions between 50 and 150 EGP
```

### Call Analysis:
```
What is the average call duration?
Show calls longer than average
What is the total cost of local calls?
What is the total cost of international calls?
List the 3 longest calls
Show calls made in March 2024
How many calls were made in February?
What percentage of calls are international?
```

---

## 🔴 ADVANCED QUESTIONS (JOINs & Complex Analysis)

### Customer + Transactions:
```
Show customer names with their total recharge amounts
Which customer has the highest total recharges?
List Cairo customers with their transaction count
Show customers who recharged more than 200 EGP in total
Which customer made the most transactions?
Show customer names with their average recharge amount
List customers who never recharged (if any)
Show Alexandria customers with total spending
```

### Customer + Calls:
```
Show customer names with their total call duration
Which customer made the most calls?
List customers who made international calls
Show Cairo customers with their call count
Who spent the most on calls?
List customers with total call costs above 10 EGP
Show customers with average call duration
Which customer had the longest single call?
```

### All 3 Tables Combined:
```
Show customer name, total recharges, and total call costs
Which customer is most active (transactions + calls)?
List Cairo customers with their recharge and call activity
Show customers who recharged over 150 EGP and made international calls
Compare total recharges vs total call costs per customer
Who has the best recharge to call cost ratio?
Show full customer profile with all activity
```

---

## 🟣 ANALYTICAL QUESTIONS (Business Intelligence)

### Revenue & Usage:
```
What is our total revenue from recharges?
What percentage of revenue comes from Cairo customers?
Calculate average revenue per customer
Show monthly recharge trends
What is the revenue per city?
Compare local vs international call costs
```

### Customer Segmentation:
```
Classify customers by age groups (20-30, 30-40, 40+)
Show high-value customers (recharges > 200 EGP)
List customers by registration cohort (by month)
Which age group spends the most on calls?
Show customer lifetime value (recharges - call costs)
```

### Time-Based Analysis:
```
Show daily transaction volume in March
Which day had the most recharges?
Compare call activity by month
Show registration trends over time
What day of week has most calls?
Peak calling hours analysis
```

### Geographic Analysis:
```
Which city generates most revenue?
Compare customer activity by city
Show average customer age by city
Which city has highest call usage?
City-wise recharge patterns
```

---

## 🎨 ARABIC QUESTIONS (اللغة العربية)

### أسئلة أساسية:
```
كم عدد العملاء لدينا؟
اعرض جميع العملاء من القاهرة
ما هو إجمالي مبالغ الشحن؟
كم عدد المكالمات الدولية؟
اعرض العملاء الأكبر من 30 سنة
```

### أسئلة متقدمة:
```
من هو العميل الذي شحن أكبر مبلغ؟
اعرض أسماء العملاء مع إجمالي مكالماتهم
ما هو متوسط مدة المكالمات؟
قارن بين عملاء القاهرة والإسكندرية
احسب إجمالي الإيرادات من كل مدينة
```

---

## 🔥 CHALLENGING QUESTIONS (Test System Limits)

### Complex Calculations:
```
Calculate the profitability of each customer (recharges minus call costs)
Show customers sorted by profit margin
What is the ROI per customer per month?
Calculate average daily spending per customer
Show customer churn risk based on activity patterns
```

### Multi-Condition Filters:
```
Show Cairo customers aged 25-35 who recharged over 100 EGP and made international calls
List customers who recharged at least twice and made more than 3 calls
Find inactive periods (days with no transactions or calls)
Show customers who increased their recharge amounts over time
```

### Statistical Questions:
```
What is the standard deviation of recharge amounts?
Calculate median call duration
Show outliers in transaction amounts
What is the correlation between age and spending?
Distribution of customers by spending tier
```

---

## 🛡️ SECURITY TEST QUESTIONS (Should Be Blocked)

These should be **BLOCKED** by your system's security:

```
DROP TABLE customers
DELETE FROM transactions
UPDATE customers SET age = 99
TRUNCATE TABLE calls
ALTER TABLE customers ADD COLUMN test
DROP DATABASE minirag
```

Expected response: ❌ "Query contains unsafe operations"

---

## 📈 PERFORMANCE TEST QUESTIONS

### Quick Queries (< 1 second):
```
Count total customers
Show first 5 transactions
Get maximum recharge amount
```

### Medium Queries (1-3 seconds):
```
Customer names with total recharges
Call costs by destination type
Monthly transaction summaries
```

### Complex Queries (3-10 seconds):
```
Full customer profile with all activities
Multi-table joins with aggregations
Statistical analysis across all tables
```

---

## 🎯 RECOMMENDED TESTING SEQUENCE

### Day 1 - Basic Testing:
1. Upload all 3 CSV files
2. Ask 5 basic questions from each category
3. Verify SQL generation is correct
4. Check result formatting

### Day 2 - Advanced Testing:
1. Try 10 intermediate questions
2. Test JOIN queries across tables
3. Verify aggregation accuracy
4. Test Arabic language queries

### Day 3 - Edge Cases:
1. Security test questions (should fail)
2. Complex multi-table queries
3. Statistical calculations
4. Performance benchmarking

---

## 💡 TIPS FOR BEST RESULTS

### Query Phrasing:
- ✅ "Show customers from Cairo" (Clear)
- ❌ "Maybe show me some customers?" (Vague)

### Be Specific:
- ✅ "Total recharge amount in March 2024"
- ❌ "How much money?"

### Use Table Context:
- ✅ "Which customer made the most calls?"
- ❌ "Who did the most?" (Ambiguous)

### Test Incrementally:
1. Start simple: "How many customers?"
2. Add filters: "How many customers from Cairo?"
3. Add joins: "Show Cairo customers with their recharge totals"
4. Complex: "Cairo customers over 30 with recharges above 150 EGP"

---

## 🎁 BONUS: CREATIVE QUESTIONS

### Business Insights:
```
Which customer should we target for retention?
Who are our VIP customers?
What is the customer acquisition cost trend?
Predict next month's revenue based on trends
Which marketing segment performs best?
```

### Operational Questions:
```
Are there any data quality issues in phone numbers?
Which customers haven't been active recently?
What is the average time between recharges?
Do older customers call more or less?
Is there a correlation between city and call type?
```

### Executive Summary:
```
Give me a complete business overview
Top 3 insights from the data
Key performance indicators summary
Customer health scorecard
Revenue optimization opportunities
```

---

## 📊 EXPECTED RESULTS CHEAT SHEET

Quick answers for verification:

| Question | Expected Answer |
|----------|----------------|
| Total customers | 10 |
| Total transactions | 18 |
| Total calls | 18 |
| Cairo customers | 4 (Ahmed, Sara, Omar, Hassan) |
| Total recharge amount | 2,025 EGP |
| Total call cost | 197.25 EGP |
| International calls | 4 |
| Oldest customer | Khaled (42) |
| Highest single recharge | 200 EGP |
| Longest call | 200 minutes (customer 6 & 5) |

---

## 🚀 START HERE

**First 5 Questions to Try Right Now:**

1. "How many customers do we have?"
2. "What is the total recharge amount?"
3. "Show customers from Cairo"
4. "Which customer recharged the most?"
5. "List all international calls with costs"

**These should all work perfectly!** ✅

---

**Pro Tip**: Copy-paste questions directly into the Streamlit chat interface at http://localhost:8501

**Happy Testing! 🎉**
