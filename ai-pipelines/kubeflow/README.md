## Setting Up Kaggle Credentials

Before running the pipeline, you must create a Kubernetes secret that holds your Kaggle credentials.

1. **Create a `kaggle.json` file** with the following contents (replace the dummy values `"dummy-user"` and `"dummy-key"` with your actual Kaggle username and key):
   ```json
   {
     "username": "dummy-user",
     "key": "dummy-key"
   }
   ```

2. Create the Kubernetes secret:
```
oc create secret generic kaggle-secret --from-file=kaggle.json
```

Make sure this secret is created before you run your pipeline so that the Kaggle credentials will be available for the data download step.


