from flask import Flask 
from flask_restful import Api, Resource, reqparse, abort
app = Flask (__name__)
api = Api(app)


# input validation post devices
devices_post_args = reqparse.RequestParser();
devices_post_args.add_argument("id", type=str, help="id input !!", required=True)
devices_post_args.add_argument("airplane_id", type=str, help="airplane_id input !!", required=True)
devices_post_args.add_argument("serial_number", type=str, help="serial_number input !!", required=True)
devices_post_args.add_argument("description", type=str, help="description input !!", required=True)



# input validation PATCH  devices/{id}
devices_patch_args = reqparse.RequestParser();
devices_patch_args.add_argument("airplane_id", type=str, help="airplane_id input !!", required=True)
devices_patch_args.add_argument("serial_number", type=str, help="serial_number input !!", required=True)
devices_patch_args.add_argument("description", type=str, help="description input !!", required=True)



devices = [ {
        "id": "device01",
        "airplane_id": "airplane1",
        "serial_number": "5234934889",
        "description": "That’s a great device",
          "deleted" : False
    },
    {
        "id": "device02",
        "airplane_id": "airplane2",
        "serial_number": "5234934889",
        "description": "That’s a great device",
          "deleted" : False
    }]

airplanes= [
   "no_airplane",
   "airplane1",
   "airplane2",
   "airplane3",
   "airplane4"
]


class DeviceId (Resource):
    
    
    # get requset with device id 
    def get(self, device_id):
    
        # go over all devices and check if input id match device id 
        # check if device not deleted
        # check if deviec airplane_id exist in airplanes array
        for device in devices:
            if device['id'] == device_id and not device['deleted'] and device['airplane_id'] in airplanes:
                # found match id - save device attribute without delete 
                
                return {
                        "id": device['id'],
                        "airplane_id": device['airplane_id'],
                        "serial_number": device['serial_number'],
                        "description": device['description'],
                        }   
        
        # if we get here it is mean that device id not found         
        abort(404, message="devices not found")
        
            
    # PATCH requset update device
    def patch(self, device_id):
    
        # get patch arguments and check validation
        args = devices_patch_args.parse_args()
        for device in devices:
            # check if device id found and not delete
            if device['id'] == device_id and device['deleted']:
                abort(404, message="devices not found")
            
            if device['id'] == device_id:
                # update device 
                device['airplane_id'] = args['airplane_id']
                device['serial_number'] = args['serial_number']
                device['description'] = args['description']
                
                return "device updated successfully" , 201
    
        # if we get here it is mean that device id not found         
        abort(404, message="devices not found")

    
    # delete requset update device
    def delete(self, device_id):
        
        # find device and set delete field true
        for device in devices:
            if device['id'] == device_id:
                device['deleted'] = True
                return "device deleted successfully" , 201
        
        # if we get here it is mean that device id not found         
        abort(404, message="devices not found")
                

class Devices (Resource):
    
    
    def get(self): 

        # array of json - devices exist in airplanes
        return_devices=[]
        # check if device id exist in airplanes and not deleted
        for device in devices:
            if device["airplane_id"] in airplanes and not device["deleted"]:
                # create new json without delete field
                return_devices.append({
                    "id": device['id'],
                    "airplane_id": device['airplane_id'],
                    "serial_number": device['serial_number'],
                    "description": device['description'],
                })
        
        # check if devices not empty 
        if not return_devices:
            abort(404, message="devices not found")
       
        return return_devices
        
    
    def post(self):
        
        # get posted argument and check validation
        args = devices_post_args.parse_args()
        # find if device id or serial_number exist
        for device in devices:
            if device['id'] == args['id'] or device['serial_number'] == args['serial_number']:
                abort(409, message="device already exist!!")
        
        # add delete field to json
        args['deleted'] = False
        
        # add device to list and return status 201
        devices.append(args);
        return "device added successfully" , 201
    
api.add_resource(Devices, "/devices")
api.add_resource(DeviceId, "/devices/<string:device_id>")



if __name__ == "__main__":
    app.run(debug = True)
    