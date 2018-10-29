import boto3
import datetime

today = datetime.date.today()
todayString = today.strftime('%Y/%m/%d')

#Delete snapshots after 4 days
deleteAfterDays = 4 
deleteDay = today - datetime.timedelta(days=deleteAfterDays)

ec2 = boto3.client('ec2')
regions = ec2.describe_regions().get('Regions',[] )
allRegions = [region['RegionName'] for region in regions]

def lambda_handler(event, context):
    snapshotCount = 0
    snapsizeCount = 0
    deleteCount = 0
    deleteSizeCount = 0

    for region in allRegions:
      print('EC2 Region instance {0}:'.format(region))
      ec2 = boto3.resource('ec2', region_name=region)
      # Instances with auto_snapshot == true
      ec2Instances = ec2.instances.filter(Filters=[{'Name': 'tag:InstanceBackup', 'Values': ['Yes']}])
          
      volumeIds = []
      for i in ec2Instances.all():
          for tag in i.tags: 
              if tag['Key'] == 'Name':
                  name = tag['Value']
          vols = i.volumes.all() 
          for v in vols:
              print('{0} attached to volume {1}, taking snapshot'.format(name, v.id))
              volumeIds.extend(v.id)
              snapshot = v.create_snapshot(Description = 'AutoSnapshot of {0}, on volume {1} - Created {2}'.format(name, v.id, todayString),)
              snapshot.create_tags(Tags = [{'Key': 'auto_snap',
                                            'Value': 'true' },
                                           {'Key': 'volume',
                                            'Value': v.id },
                                           {'Key': 'CreatedOn',
                                            'Value': todayString },
                                           {'Key': 'Name',
                                            'Value': '{} autosnap'.format(name)}])
              print('Snapshot Done')
              snapshotCount += 1
              snapsizeCount += snapshot.volume_size
              snapshots = ec2.snapshots.filter(Filters=[{'Name': 'tag:auto_snap', 'Values': ['true']}])
              for snap in snapshots:
                  canDelete = False
                  for tag in snap.tags:
                      if tag['Key'] == 'CreatedOn':
                          createdOnString = tag['Value']
                      if tag['Key'] == 'auto_snap':
                          if tag['Value'] == 'true':
                              canDelete = True
                      if tag['Key'] == 'Name':
                          name = tag['Value']
                  createdOn = datetime.datetime.strptime(createdOnString, '%Y/%m/%d').date()
                  if createdOn <= deleteDay and canDelete == True:
                      deleteSizeCount += snap.volume_size
                      snap.delete()
                      deleteCount += 1
    print('Made {0} snapshots of {1} GB\
           Deleted {2} snapshots of {3} GB'.format(snapshotCount, snapsizeCount, deleteCount, deleteSizeCount))
    return
