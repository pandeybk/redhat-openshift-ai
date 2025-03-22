# Using a Custom Elyra Image and MinIO Data Connection on Red Hat OpenShift Data Science

We are going to cover following
1. **Importing** a custom Elyra notebook image (`quay.io/eformat/elyra-base:0.2.1`) into Red Hat OpenShift Data Science (RHODS).
2. **Creating** a new workbench that uses this custom image.
3. **Setting up** a MinIO data connection.
4. **Storing** Kaggle credentials for use in pipelines.

---

## 1. Import the Custom Notebook Image
![Import custom image](./assets/import-custom-image.png)

1. In RHODS, navigate to **Settings** → **Notebook images**.
2. Click **Import** to add a new notebook image.
3. Under **Image location**, type or select: `elyra-pipeline-local-run` 
(Adjust as needed for your environment.)
4. Under **Name**, specify the image reference, for example: `quay.io/eformat/elyra-base:0.2.1`
5. (Optional) Add a **Description** or any relevant details.
6. Click **Import**.

---

## 2. Create a Workbench Using the Custom Image
![Create workbench using custom image](./assets/create-workbench.png)
1. Go to **Data Science Projects** in RHODS and open or create your project.
2. Click **+ Create Workbench** (or **Create** if you’re making a brand new one).
3. Give the workbench a name and choose the **Notebook image** you just imported: `quay.io/eformat/elyra-base:0.2.1`
4. Select the desired **Deployment size** (CPU/Memory).
5. (Optional) Provide any **Environment variables** you need for local configuration.
6. Click **Create** or **Update**.

---

## 3. Create (or Attach) the MinIO Data Connection
![Create data connection](./assets/create-data-connection.png)
During workbench creation (or while editing it later):
1. Scroll down to **Connections**.
2. Click **Create connection** or **Attach existing connections**.
3. Select **S3 compatible object storage** for **Type**.
4. Fill in the details for your MinIO instance:
   - **Name**: e.g. `minio`
   - **Access key**: `minio`
   - **Secret key**: `minio123`
   - **Endpoint**: `http://minio-service.netsentinel:9000`
   - **Region**: `us-east-1` (or any default)
   - **Bucket**: Use a valid bucket name. Example `predictive-model-training`
5. Click **Create** or **Attach**. The connection should now be listed under **Connections**.

---

## 4. Store Kaggle Credentials
If you need to download datasets from Kaggle within this workbench or pipeline, provide a Kaggle API token in: `/opt/app-root/src/.config/kaggle/kaggle.json`

### Steps:
1. Generate your API token from [Kaggle](https://www.kaggle.com/) (Profile → Account → Create New API Token).
2. In your workbench terminal or via a script, create the folder and file:
```
mkdir -p /opt/app-root/src/.config/kaggle 
cat <<EOF > /opt/app-root/src/.config/kaggle/kaggle.json 
{ "username": "YOUR_KAGGLE_USERNAME", "key": "YOUR_KAGGLE_KEY" } 
EOF 
chmod 600 /opt/app-root/src/.config/kaggle/kaggle.json
```
3. Verify the file exists:
```
cat /opt/app-root/src/.config/kaggle/kaggle.json
```
4. Your Kaggle scripts should now authenticate automatically.
