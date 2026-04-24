This implementation plan is organized into modular blocks that align the front-end user experience with the specific backend (BE) logic required for each stage of the Babel Fish workflow.

---

## **Babel Fish: Technical Implementation Plan**

### **Module 0: Goal Selection & Seed Data Upload**
**UI Screen:** *0. Goal Selection & Upload*
* **Chain of Thought (CoT):** The agent identifies the campaign's "North Star" to determine which Google signals are relevant for the final script. The uploaded data serves as the raw source for all subsequent translations.
* **Front-End Action:** User selects a campaign goal (e.g., Reach & Brand Lift) and drags/drops the CSV seed data.
* **BE Logic Block (Data Profiling & Caching):**
    * **Validation:** Scans the CSV to define column formats and identify structural gaps.
    * **Caching:** Data is cached in memory via built-in http.server (no persistent storage) to be used in subsequent steps.
    * **Preview:** Returns the top 5 rows of the uploaded CSV for dynamic visualization in the frontend.
* **Detailed Implementation Plan:**
    * **Backend:** Create `server.py` in the folder using built-in http.server. It will handle file upload and return the top 5 rows.
    * **Frontend:** Update `goal.html` to handle goal selection, file upload via AJAX/Fetch, and dynamic table rendering based on the backend response.
* **Deliverable:** Data Profiling & Hygiene Report (simulated or basic) and Dynamic Data Preview.

---

### **Module 1: 1:1 General Field Translation**
**UI Screen:** *1. Core Identifier Mapping*
* **CoT:** The agent identifies "low-hanging fruit"—fields with direct, high-confidence equivalents in the Google Signal schema—before moving to complex logic.
* **Front-End Action:** User reviews proposed matches and approves them for the next step.
* **BE Logic Block (Baseline Check & Keyword Matching):**
    * **Universal Baseline Check:** Matches standard fields like `domain`, `channels` that are visible on both client and Google systems.
    * **Keyword Matching:** Uses non-absolute keyword matching (fuzzy matching) to cross-reference client column names against the master Google ID JSON schema (`google_signal.json`).
* **Detailed Implementation Plan:**
    * **Backend:** Create `server.py` in the folder using built-in `http.server` on port 8004. It will load the CSV headers and the JSON schema, perform matching, and return the results.
    * **Frontend:** Update `mapping.html` to fetch the mappings and render them dynamically in the grid.
* **Deliverable:** Validated 1:1 Mapping Schema.

---

### **Module 2: Multi-Signal Mapping & Aggregation**
**UI Screen:** *2. Complex Mapping & Aggregation*
* **Architecture Strategy**: This block acts as a logical middleware that consolidates disparate client attributes into unified Google identifiers.
* **CoT:** Complex client data (e.g., Location + Ethnicity) is "translated" into unified Google signals through many-to-many relationship logic.
* **Front-End Action:** User defines relationship logic for complex matches.
* **BE Logic Block (Aggregation & Gap Resolution):**
    * **Signal Translation**: Maps multiple client columns into a single Google Signal.
    * **Normalization**: Strips leading/trailing spaces from headers and values.
    * **Memory Management**: Reads the file from GCS in chunks to avoid memory overflow.
    * **Aggregation Logic**: Clusters data points to define volume, enforcing a minimum user threshold.
* **Specific Mapping Logic (Step 2):**
    * **Location** ➔ `City_id`, `country_code`, `country_id`, `dma_id`, `zip_postal_code` (Relationship: One-to-Many | Match: Direct | Action: Select)
    * **Broad_interest_category** ➔ `adx page categories`, `Channels` (Relationship: One-to-Many | Match: Direct | Action: Select)
    * **Ethnicity group** ➔ `Language`, `country_id` (Relationship: One-to-Many | Match: Direct | Action: Select)
    * **Credit Score** ➔ Google Signal (Undetected) (Relationship: Data Input | Match: Aggregated | Action: Select)
* **Deliverable:** Structured summary of complex mapping logic.

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

### **Module 4: Automated Script Generation**
**UI Screen:** *4. Review & Deploy*
* **CoT:** The modeling weights and mapping schema are converted into a technical script that adheres to strict Google Python grammar.
* **Front-End Action:** User clicks "Generate Script" and reviews the Python code in the preview window.
* **BE Logic Block (Code Generation):**
    * **Grammar Enforcement:** Generates a Python 3 script that strictly avoids loops, relying on linear logic and built-in functions like `sum_aggregate` or `max_aggregate`.
    * **Technical Constraints:** Ensures all custom variables are prefixed with an underscore to avoid system collisions.
* **Deliverable:** Executable Python 3 Custom Bidding Script.

---

### **Module 5: DV360 API Integration**
**UI Screen:** *5. Final Review & Deployment*
* **CoT:** The final automation step pushes the validated script directly to the advertising platform to eliminate manual deployment errors.
* **Front-End Action:** User selects "Push to DV360 API".
* **BE Logic Block (Deployment):**
    * **Syntax Verification:** Runs a final check through the script verification server to ensure it is error-free before deployment.
    * **API Push:** Deterministic final step where the agent pushes the generated script to the DV360 API endpoints.
* **Deliverable:** Confirmation of successful deployment to the DV360 account.