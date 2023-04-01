while true; do
  scp -i /data/secrets/credentials/holdings-kevin.pem ec2-user@18.116.40.104:/home/ec2-user/ASL_Classification.ipynb .
  scp -i /data/secrets/credentials/holdings-kevin.pem ec2-user@18.116.40.104:/home/ec2-user/training_classifier_asl.h5 training_classifier_asl.h5
  git add .
  git commit -m .
  git push
  sleep 900
done
