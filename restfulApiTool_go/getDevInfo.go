package main

import (
    "fmt"
    "restful"
)

func getToken(token chan string) {
    uap := &restful.Uap{
	    HostSite: "mptw.com.tw",
        ClientId: "REMOVE FOR CREDENTIAL",
	    ClientSecret: "REMOVE FOR CREDENTIAL",
    }
    uap.GetUserToken("twmp@test.com", "******")
    token <- uap.UserToken
}

func main() {

    uap := &restful.Uap{
	    HostSite: "mptw.com.tw",
        ClientId: "REMOVE FOR CREDENTIAL",
	    ClientSecret: "REMOVE FOR CREDENTIAL",
    }
    uap.GetUserToken("twmp@test.com", "******")
    fmt.Printf("User token: %s\n", uap.UserToken)
    uap.ListDevice()
    data := uap.Response.JsonData.(restful.ResListDevice)
    fmt.Println(uap.Response.StatusCode)
    fmt.Println(uap.Response.Speed)
    fmt.Println(data.Data[0].DeviceName)


    var devSlice []string
    //devSlice = append(devSlice, data.Data[0].MydlinkId)
    
    for _, device := range data.Data {
        devSlice = append(devSlice, device.MydlinkId)
    }
    
    fmt.Println(devSlice)

    uap.GetDeviceInfo(devSlice)
    data2 := uap.Response.JsonData.(restful.ResGetDevInfo)
    for _, device := range data2.Data {
        fmt.Printf("MydlinkID: %s\n", device.MydlinkId)
        fmt.Printf("PromLevel: %d\n", device.PromotionInfo.Level)
    }
}
