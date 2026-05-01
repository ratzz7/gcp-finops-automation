import google.cloud.compute_v1 as compute_v1

def identify_unattached_disks(project_id: str):
    disk_client = compute_v1.DisksClient()
    # Use AggregatedList to scan across ALL zones in the project
    request = compute_v1.AggregatedListDisksRequest(project=project_id)
    
    unattached_disks = []
    
    # Aggregated list returns a paginated list of (zone, disks_in_zone)
    for zone, response in disk_client.aggregated_list(request=request):
        if response.disks:
            for disk in response.disks:
                # If users list is empty, the disk is unattached
                if not disk.users:
                    unattached_disks.append({
                        "name": disk.name,
                        "zone": zone.split('/')[-1],
                        "size_gb": disk.size_gb
                    })
            
    return unattached_disks

if __name__ == "__main__":
    PROJECT_ID = "responsive-icon-346114"
    print(f"Scanning project {PROJECT_ID} for orphaned disks...")
    try:
        results = identify_unattached_disks(PROJECT_ID)
        if results:
            print(f"\nSUCCESS: Found {len(results)} orphaned disks:")
            for d in results:
                print(f" - {d['name']} ({d['size_gb']}GB) in {d['zone']}")
        else:
            print("\nScan complete: No orphaned disks found.")
    except Exception as e:
        print(f"\nERROR: {e}")
