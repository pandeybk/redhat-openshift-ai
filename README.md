# **Red Hat OpenShift AI Product Demo - Customer Presentation Guide**

## **1. Installation Process and Required Operators**

### **What is it?**

- OpenShift AI requires several operators to manage AI/ML workloads efficiently.
- These operators provide GPU acceleration, model serving, storage, and pipeline automation.

### **Problems it Solves**

- ✔️ Simplifies AI/ML infrastructure setup by automating complex configurations.
- ✔️ Ensures scalability, security, and reliability for AI workloads.

### **Key Discussion Areas**

- OpenShift AI integrates with OperatorHub for streamlined deployment.
- Required Operators:
  - [ ] **Red Hat OpenShift AI** – Core AI/ML platform.
  - [ ] **NVIDIA GPU Operator** – Manages GPU acceleration.
  - [ ] **Node Features Discovery Operator** – Detects hardware capabilities.
  - [ ] **Serverless Operator**
        – Enables **Knative Serving**, which is a foundation for event-driven, autoscaled workloads, and KServe is built on top of Knative.
        -  KServe handles single and multi-model serving and leverages Knative (enabled by Serverless Operator) for features like autoscaling and revisions.
  - [ ] **Service Mesh Operator** – Controls traffic and security for AI models, manage multi model server
  - [ ] **Storage Class/Controller Setup** – Manages persistent storage.
  - [ ] **Authorino Operator** – Handles API authentication and authorization.
  - [ ] **Tekton Pipeline Operator** – Automates AI pipeline execution.

---

## **2. DataScienceCluster Initialization**

### **What is it?**

- The core framework for orchestrating AI/ML workloads in OpenShift AI.

### **Key Discussion Areas**

- [ ] Provides a centralized way to manage AI workloads.
- [ ] Users can **enable or disable** specific OpenShift AI components based on requirements.

---

## **3. RHOAI Authentication**

### **What is it?**

- Authentication system to manage user access within OpenShift AI.

### **Problems it Solves**

- ✔️ Ensures secure access control for AI/ML workloads.
- ✔️ Integrates seamlessly with enterprise authentication systems.

### **Key Discussion Areas**

- OpenShift AI supports multiple authentication methods:
  - [ ] **OpenShift Native Authentication, Basic Authentication, LDAP, HTPasswd, OAuth, GitHub, GitLab, Google, Keystone, OpenID Connect, Request Header Authentication**
- Enterprises can leverage existing authentication mechanisms for seamless access control.

---

## **4. Data Science Projects**

### **What is it?**

- A structured way to organize AI/ML resources within OpenShift AI.
- Apply all OCP namespace construct like, resourcequotas, limitrange, network policies, rbac policies etc.

### **Problems it Solves**

- ✔️ Provides a project-based structure to manage AI/ML workloads efficiently.
- ✔️ Enables role-based access control for different teams.

### **Key Discussion Areas**

- **Core Components:**
  - [ ] **Workbenches** – Interactive development environments.
  - [ ] **Pipelines** – Automates model training and deployment.
  - [ ] **Models** – Centralized model management.
  - [ ] **Cluster Storage** – Persistent storage for AI workloads.
  - [ ] **Data Connections** – Secure external data integration.
  - [ ] **Permissions** – Controlled access for users and groups.
- [ ] Users can **create and delete projects** based on their AI/ML needs.

---

## **5. Workbenches**

### **What is it?**

- Interactive development environments for data scientists.
- Supports **Jupyter Notebooks**, **VSCode**, and **R Studio** with custom images.

### **Problems it Solves**

- ✔️ Reduces setup time by providing pre-configured environments.
- ✔️ Ensures reproducibility and consistency in AI workflows.

### **Key Discussion Areas**

- [ ] **Jupyter Notebooks Setup** – Standard tool for AI/ML development.
- [ ] **Code Server Setup** – Browser-based VS Code for ML engineering.
- [ ] **Custom Images for R Studio** – Support for R-based workflows.
- [ ] **Version Control** – Integrated Git support.
- [ ] **Install add-ons and plugins** – To extend functionality.

---

## **6. Pipelines**

### **What is it?**

- Automated workflows for AI/ML model training and deployment.

### **Problems it Solves**

- ✔️ Reduces manual effort by automating data processing and model training.
- ✔️ Ensures consistency and efficiency in ML workflows.

### **Key Discussion Areas**

- [ ] **Kubeflow Pipeline Demo** – Training an ML model using the **UNSW-NB15 dataset**.
- [ ] **Uploading to S3 Bucket** – Storing processed data and models.
- [ ] **Elyra Pipeline Demo** – Jupyter Notebook-based pipeline alternative.

---

## **7. Models**

### **What is it?**

- Model management and deployment framework within OpenShift AI.

### **Problems it Solves**

- ✔️ Provides a standardized way to deploy and manage AI models.
- ✔️ Enables GPU-accelerated inference for real-time applications.

### **Key Discussion Areas**

- [ ] **Deploying ONNX Models** using **OpenVINO Model Server**.
- [ ] **Custom Model Server Setup** with **NVIDIA Triton**.
- **Single vs. Multi-Model Servers**:
  - [ ] **Single Model Server** – Deploys one model at a time.
  - [ ] **Multi-Model Server** – Hosts multiple models in a shared environment.
- [ ] **Predictive Model Deployment** – Deploy ONNX model in OpenVINO Model server.
- [ ] **LLM Deployment** – Not included in this demo due to resource constraints.

---

## **8. Cluster Storage**

### **What is it?**

- Persistent storage system for AI/ML workloads.

### **Problems it Solves**

- ✔️ Ensures AI models and datasets are stored securely.
- ✔️ Provides flexibility in choosing different storage classes.

### **Key Discussion Areas**

- [ ] **CSI Controller** – Manages persistent volume claims.
- [ ] **Multiple Storage Classes** – Configurable based on performance needs.

---

## **9. Data Connections**

### **What is it?**

- Mechanisms for integrating external data sources into OpenShift AI.

### **Problems it Solves**

- ✔️ AI workloads rely on large datasets from multiple sources.
- ✔️ Provides secure and scalable data integration.

### **Key Discussion Areas**

- [ ] **S3 Bucket Connection** – Connect internal/external object storage.
- [ ] **URL-based Data Access** – Fetch datasets from online sources.

---

## **10. Permissions**

### **What is it?**

- Role-based access control (RBAC) for OpenShift AI.

### **Problems it Solves**

- ✔️ Ensures proper governance and security of AI resources.
- ✔️ Prevents unauthorized access to sensitive workloads.

### **Key Discussion Areas**

- [ ] **Sample Users and Groups** – Demonstrating access control.
- [ ] **Granular Permission Settings** – Restricting or allowing operations at various levels.

---

## **11. NVIDIA GPU and Node Feature Discovery Operator**

### **What is it?**

- This integration manages, optimizes, and exposes GPU capabilities within OpenShift AI.
- Combines the power of the **NVIDIA GPU Operator** with the **Node Feature Discovery (NFD) Operator** to detect and configure hardware features, enabling efficient use of GPU resources for AI/ML workloads.

### **Problems it Solves**

- ✔️ **Simplifies GPU Lifecycle Management**: Automates the installation, configuration, and monitoring of NVIDIA GPU drivers and runtimes on OpenShift nodes.
- ✔️ **Enables Hardware-Aware Scheduling**: With NFD, nodes are labeled with detailed hardware capabilities, enabling the scheduler to place AI workloads appropriately.
- ✔️ **Supports Advanced GPU Sharing**: Provides access to MIG (Multi-Instance GPU) and time slicing, allowing multiple workloads to run on the same GPU efficiently.
- ✔️ **Improves Cluster Resource Utilization**: Enables fine-grained GPU resource allocation to maximize throughput and cost-efficiency.

### **Key Discussion Areas**

- [ ] **Node Feature Discovery Operator** – Scans and labels nodes with hardware-specific attributes like GPU model, MIG support, memory, and more. Essential for enabling intelligent scheduling of GPU workloads.
- [ ] **Accelerator Profiles** – Customizable configurations for GPU workloads, allowing you to define how GPUs are exposed (e.g., full GPU, MIG slice, time-sliced).
- [ ] **Time Slicing** – Allows a single GPU to be shared across multiple AI jobs in a time-based manner, improving resource utilization.
- [ ] **MIG (Multi-Instance GPU)** – Physically partitions a single NVIDIA A100/H100 GPU into multiple smaller, isolated instances for multi-tenant or parallel workloads.

---

## **12. Monitoring**

### **What is it?**

- Observability tools for tracking GPU and AI workload performance.

### **Problems it Solves**

- ✔️ Ensures AI workloads run optimally.
- ✔️ Provides visibility into system performance.

### **Key Discussion Areas**

- [ ] **Custom DGCM Dashboard** – Real-time GPU monitoring.
- [ ] **Performance Metrics** – Track AI job execution and resource utilization.

---

## **13. Future Discussion**

- [ ] **Distributed Training** – Ray Cluster/Code Flare SDK.
