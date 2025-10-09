# 🚀 Quick Start Testing Guide for Text-to-SQL Feature

## 📋 Prerequisites

1. **Install Dependencies**
```powershell
cd c:\University\Mini_RAG\mini-rag-app\src
pip install pandas==2.2.3 openpyxl==3.1.5
```

2. **Restart Backend**
```powershell
# Stop backend if running (Ctrl+C)
cd c:\University\Mini_RAG\mini-rag-app\src
python main.py
```

3. **Start SQL Chat App**
```powershell
cd c:\University\Mini_RAG\mini-rag-app\streamlit_app
streamlit run app_sql_chat.py
```

---

## 📊 Sample Data Included

I've created 3 ready-to-use CSV files:

### 1. `customers.csv` (10 customers)
- customer_id, name, phone, email, city, age, registration_date
- Egyptian customer data with Cairo, Alexandria, Giza locations

### 2. `transactions.csv` (18 recharge transactions)
- transaction_id, customer_id, phone, amount, transaction_type, transaction_date, status
- Recharge history from January to March 2024

### 3. `calls.csv` (18 call records)
- call_id, customer_id, phone, call_duration_minutes, call_date, destination_type, call_cost
- Local and international calls

---

## 🧪 Testing Scenarios

### **Test 1: Upload Datasets**

1. In sidebar → **📁 Dataset Upload** section
2. Upload `customers.csv`:
   - Click "Choose a CSV or Excel file"
   - Select `sample_data/customers.csv`
   - Click "📤 Upload Dataset"
   - Should see: "✅ Dataset uploaded: 10 rows"

3. Upload `transactions.csv`:
   - Repeat process
   - Should see: "✅ Dataset uploaded: 18 rows"

4. Upload `calls.csv`:
   - Repeat process
   - Should see: "✅ Dataset uploaded: 18 rows"

5. **Verify Tables**:
   - Check **📊 Uploaded Tables** section
   - Should see 3 tables: `dataset_customers`, `dataset_transactions`, `dataset_calls`

---

### **Test 2: Basic SQL Queries (Auto Mode)**

Set mode to **🔮 Auto-Detect** in sidebar, then ask:

#### Count Queries:
1. "How many customers do we have?"
   - ✅ Expected: 10 customers
   
2. "How many transactions are completed?"
   - ✅ Expected: 18 transactions

3. "How many calls were international?"
   - ✅ Expected: 4 international calls

#### Simple Filters:
4. "Show me all customers from Cairo"
   - ✅ Expected: 4 customers (Ahmed, Sara, Omar, Hassan)

5. "List all recharges over 150 EGP"
   - ✅ Expected: 6 transactions (200 and 150 amounts)

6. "Show customers older than 35"
   - ✅ Expected: 4 customers (ages 36, 39, 42)

---

### **Test 3: Aggregation Queries**

7. "What's the total recharge amount?"
   - ✅ Expected: 2,025.00 EGP

8. "What's the average call duration?"
   - ✅ Expected: ~107.5 minutes

9. "Show total recharge by customer"
   - ✅ Expected: Table with customer_id and sum amounts

10. "What's the maximum recharge amount?"
    - ✅ Expected: 200.00 EGP

---

### **Test 4: JOIN Queries (Advanced)**

11. "Show customer names with their total recharges"
    - ✅ Should join customers + transactions
    - Display: name, total_amount

12. "Which customers made international calls?"
    - ✅ Should join customers + calls
    - Display: names of customers with destination_type='international'

13. "Show customers from Cairo with their transaction count"
    - ✅ JOIN with WHERE clause
    - Display: Cairo customers with count

---

### **Test 5: Sorting & Limiting**

14. "Top 5 customers by total recharge amount"
    - ✅ ORDER BY with LIMIT 5

15. "Latest 10 transactions"
    - ✅ ORDER BY transaction_date DESC LIMIT 10

16. "Longest 5 calls"
    - ✅ ORDER BY call_duration_minutes DESC LIMIT 5

---

### **Test 6: Date Queries**

17. "How many transactions in March 2024?"
    - ✅ WHERE with date range

18. "Show calls made in February"
    - ✅ Date filtering

19. "Customers registered after February 1st, 2024"
    - ✅ Date comparison

---

### **Test 7: Security Tests (Should Block)**

20. "DROP TABLE customers"
    - ❌ Should see: "Query contains unsafe operations"

21. "DELETE FROM transactions"
    - ❌ Should be blocked

22. "UPDATE customers SET age = 30"
    - ❌ Should be blocked

---

### **Test 8: RAG Mode Switch**

Switch to **📄 RAG Mode**, then:

23. "What's in my documents?"
    - ✅ Should query document index (if docs uploaded)

24. "Summarize the content"
    - ✅ Should use RAG, not SQL

---

### **Test 9: UI Features**

25. **SQL Query Viewer**:
    - Expand "🔍 View SQL Query" section
    - ✅ Should show generated SQL code
    - ✅ Copy button should work

26. **CSV Download**:
    - After any query with results
    - Click "📥 Download Results as CSV"
    - ✅ Should download file

27. **Table Management**:
    - In sidebar → **📊 Uploaded Tables**
    - Click table name → See schema
    - Try deleting a table
    - ✅ Should remove from list

28. **Chat History**:
    - Create new chat: "➕ New Chat"
    - Switch between chats
    - ✅ Should preserve messages

---

## 🎯 Expected Results Summary

| Test | Query | Expected Result |
|------|-------|----------------|
| Count | "How many customers?" | 10 |
| Count | "How many transactions?" | 18 |
| Count | "International calls?" | 4 |
| Filter | "Customers from Cairo" | 4 rows |
| Filter | "Recharges > 150" | 6 rows |
| Aggregate | "Total recharge amount" | 2,025.00 |
| Aggregate | "Average call duration" | ~107.5 min |
| Join | "Customer names + total recharges" | Table with names & amounts |
| Sort | "Top 5 by recharge" | 5 customers sorted |
| Security | "DROP TABLE" | ❌ Blocked |

---

## 🐛 Common Issues & Solutions

### Issue 1: "Module not found: pandas"
```powershell
pip install pandas==2.2.3 openpyxl==3.1.5
```

### Issue 2: "404 Not Found: /api/v1/sql/..."
- Backend not restarted
- Solution: Restart `python main.py`

### Issue 3: "Upload failed"
- Check file format (CSV/Excel only)
- Check file path
- Check backend logs

### Issue 4: "Query generation slow"
- gemma2 is slow (local LLM)
- Switch to gpt-4o-mini in sidebar settings

### Issue 5: "No tables found"
- Upload datasets first
- Check **📊 Uploaded Tables** section

---

## 📊 Database Verification

To verify tables in PostgreSQL:

```sql
-- Connect to minirag database
psql -U postgres -d minirag

-- List all dataset tables
SELECT tablename FROM pg_tables 
WHERE tablename LIKE 'dataset_%';

-- Check data
SELECT * FROM dataset_customers LIMIT 5;
SELECT * FROM dataset_transactions LIMIT 5;
SELECT * FROM dataset_calls LIMIT 5;
```

---

## 🎨 UI Features to Notice

✅ **Message Bubbles**: User (right/magenta), Assistant (left/dark)
✅ **SQL Viewer**: Collapsible section with syntax highlighting
✅ **Data Tables**: Formatted DataFrames with borders
✅ **Download Button**: CSV export for all results
✅ **Mode Selector**: Auto/RAG/SQL in sidebar
✅ **Table Cards**: Show schema, samples, delete option
✅ **Chat History**: Multiple sessions with persistence
✅ **e& Branding**: Logo, colors, footer

---

## 🚀 Next Steps After Testing

1. **Try with real data**: Upload your own CSV/Excel files
2. **Test complex queries**: Multi-table JOINs, subqueries
3. **Benchmark performance**: Compare gemma2 vs gpt-4o-mini
4. **Report issues**: Note any errors or UI problems
5. **Request features**: What would make this better?

---

## 📝 Test Checklist

- [ ] Backend restarted with new routes
- [ ] Dependencies installed (pandas, openpyxl)
- [ ] App_sql_chat.py running
- [ ] All 3 sample datasets uploaded
- [ ] Tables visible in sidebar
- [ ] Basic queries working (count, filter)
- [ ] Aggregations working (sum, avg)
- [ ] JOINs working (multi-table)
- [ ] Security blocks unsafe queries
- [ ] SQL viewer showing generated code
- [ ] CSV download working
- [ ] Table management (view/delete) working
- [ ] Chat history preserved
- [ ] Mode switching (Auto/RAG/SQL) working

---

## 🎓 Query Templates

Copy these for quick testing:

```
Count Queries:
- How many [table name] do we have?
- Count all [condition]

Filters:
- Show me all [table] where [condition]
- List [table] with [field] > [value]

Aggregations:
- What's the total [field]?
- What's the average [field]?
- Sum of [field] by [group]

Sorting:
- Top [N] [table] by [field]
- Latest [N] [table]

JOINs:
- Show [table1] with their [table2]
- Which [table1] have [condition in table2]?

Dates:
- How many [table] in [month/year]?
- Show [table] after [date]
```

---

**Happy Testing! 🎉**

For issues or questions, check:
- `TEXT_TO_SQL_GUIDE.md` (comprehensive guide)
- Backend logs (FastAPI console)
- Frontend logs (Streamlit console)
- Database logs (PostgreSQL)
