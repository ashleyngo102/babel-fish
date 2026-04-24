This implementation plan details the architectural transition from raw client data to a "Google-ready" dataset, specifically focusing on the **Many-to-One Aggregation** and the handover to the **Value Modeling** engine, aligned with DV360 constraints and GCP best practices.

---

## **Babel Fish: Data Transformation & Modeling Handover**

### **Module 2.1: Many-to-One Signal Aggregation**
**UI Screen:** *2. Complex Mapping & Aggregation*
* **Architecture Strategy**: This block acts as a logical middleware that consolidates disparate client attributes into unified Google identifiers.
* **Stateless Handover (GCS)**: To handle files up to 50MB, the FE uploads the CSV directly to a GCS bucket via a Signed URL, passing only the file path to the Cloud Function.
* **Logical Execution (Cloud Function)**:
    * **Signal Translation**: Maps multiple client columns into a single Google Signal.
    * **Normalization**: Strips leading/trailing spaces from headers and values.
    * **Memory Management**: Reads the file from GCS in **chunks** (e.g., 10,000 rows) to avoid memory overflow.
    * **Aggregation Logic**: Clusters data points to define volume, enforcing a **minimum user threshold** (e.g., >= 5 users per location) to handle sparsity and noise.
* **FE State (Zustand)**: Stores the `mapping_json` and orchestrates the Signed URL upload flow. Includes a `schema_version` in the payload to prevent skew.

---

### **Module 3.0: Transition to "Transformed CSV"**
**Logic Block**: *Data Preparation (Chunked)*
* **Architecture Strategy**: Transformation occurs in-memory but is processed in chunks to maintain a low memory footprint.
* **Transformation Steps**:
    1.  **Rename**: Client-side headers are updated to match official DV360 signal names.
    2.  **Threshold Enforcement**: Filters out locations or segments with insufficient volume.
    3.  **Namespace Alignment**: Standardizes the dataset for the scoring algorithm.
* **Handover**: The aggregated results are passed to the scoring model.

---

### **Module 3.1: Weighted-Scoring Modeling**
**UI Screen:** *3. Value Modeling (Phase 1)*
* **Architecture Strategy**: Analyzes the aggregated data to derive value coefficients.
* **Statistical Execution**: Applies specific coefficients to normalized data (e.g., 50% percentage, 30% count, 20% median).
* **Output**: Produces a `value_score` for every valid location or segment.

---

### **Module 3.2: Selection-Based Value Assignment & Script Generation**
**UI Screen:** *3. Value Modeling (Phase 2)*
* **Architecture Strategy**: Finalizes the bidding values and generates the DV360 script.
* **Assignment Options**:
    * **Option A: Quantile Binning (Tiering)**: Divides locations into groups.
    * **Option B: Index Scaling**: Projects scores onto a scale.
* **DV360 Output Deliverable**: Instead of a script that calculates values dynamically, the Cloud Function generates a **Pre-computed Lookup Script** (e.g., using `first_match_aggregate` with hardcoded values for locations) to comply with DV360's 'no loops' and 'no imports' constraints.

---

### **CI/CD Integration & Deployment Reliability**
To deploy these transformations securely:
1.  **Backend Deployment**: Deploys the Python engine to **Google Cloud Functions**.
2.  **Frontend Deployment**: Pushes the React UI to **Firebase Hosting**.
3.  **Version Control**: The FE payload includes a `schema_version` header. The Cloud Function validates this version to prevent schema skew errors during staggered deployments.

**Implementation Tip**: Set the Cloud Function memory to at least 1GB to ensure smooth chunked processing of 50MB files.