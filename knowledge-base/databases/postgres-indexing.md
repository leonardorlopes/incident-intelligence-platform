# PostgreSQL Indexing Strategies

## 1. Index Types
- **B-Tree (Default):** For most use cases (equality and range queries).
- **GIN (Generalized Inverted Index):** Essential for JSONB search and full-text search.
- **BRIN (Block Range Index):** For very large tables where data is physically sorted by the index column (e.g., `created_at`).

## 2. Common Pitfalls
- **Over-indexing:** Slows down `INSERT`, `UPDATE`, and `DELETE` operations and consumes disk space.
- **Indexing Low-Cardinality Columns:** Indexing a `boolean` column is rarely beneficial as the database might prefer a sequential scan.

## 3. Covering Indexes (`INCLUDE`)
Use the `INCLUDE` clause to add non-key columns to an index, allowing for "Index-Only Scans" which avoid hitting the heap.

## 4. Partial Indexes
Create indexes on a subset of data to save space and improve performance.
`CREATE INDEX idx_active_orders ON orders (user_id) WHERE status = 'active';`

## 5. Maintenance
Regularly run `ANALYZE` and `VACUUM` to ensure the query planner has accurate statistics for choosing indexes.
