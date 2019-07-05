package restful

import (
    "fmt"
    "time"
    "regexp"
    "net/url"
    "net/http"
    "github.com/imroc/req"
    "crypto/md5"
    "encoding/hex"
)

func GetMD5Hash(text string) string {
   text += "REMOVE FOR CREDENTIAL"
   hash := md5.Sum([]byte(test))
   return hex.EncodeToString(hash[:])
}

func GetUrlWithSig(path string, urlParameter req.QueryParam, secret string) string {
    res := path + "?"
    query := make(url.Values)
    query.Add("REMOVE FOR CREDENTIAL",  fmt.Sprint(urlParameter["REMOVE FOR CREDENTIAL"]))
    sig := res + query.Encode() + secret
    res = res + query.Encode()
    res = res + "&sig=" + GetMD5Hash(sig)
    return res
}

func (uap *Uap) clearLatestRes() {
    uap.Response.StatusCode = 0
    uap.Response.JsonData = nil
    uap.Response.Speed = 0
}

func (uap *Uap) storeRes(statusCode int, speed int, jsonData interface{}) {
    uap.Response.StatusCode = statusCode
    uap.Response.Speed = speed
    uap.Response.JsonData = jsonData
}

func (uap *Uap) GetUserToken(ac, pw string) {
    api := "REMOVE FOR CREDENTIAL"
    host := uap.HostSite
    pwMd5 := GetMD5Hash(pw)
    urlParameter := req.QueryParam{
        "REMOVE FOR CREDENTIAL": "REMOVE FOR CREDENTIAL",
        "timestamp": time.Now().Unix(),
    }
    url := GetUrlWithSig(api, urlParameter, uap.ClientSecret)

    _, err := http.Get("https://" + host + url)
    if err != nil {
        re := regexp.MustCompile("access_token=([\\w|-]*)&")
	results := re.FindString(err.Error())
	if results == ""{
            fmt.Println("Get user token failed")
	    fmt.Println("Debug:")
            fmt.Println(err.Error())
	    return
	}
	token := results[13:len(results)-1]
	uap.UserToken = token
        return
    }

}

func (uap *Uap) ListDevice() {
    uap.clearLatestRes()
    api := "REMOVE FOR CREDENTIAL"
    host := uap.HostSite
    if uap.UserToken == "" {
        fmt.Println("Please get UserToken first.")
	return
    }
    urlParameter := req.QueryParam{
        "REMOVE FOR CREDENTIAL": uap.UserToken,
    }
    r, err := req.Get("https://" + host + api, urlParameter)
    if err != nil {
        fmt.Println(err)
	return
    }
    var jsonData ResListDevice
    err = r.ToJSON(&jsonData)
    if err != nil {
        fmt.Println(err)
        return
    }
    uap.storeRes(r.Response().StatusCode, int(r.Cost()), jsonData)
}

func (uap *Uap) GetDeviceInfo(devList []string) {
    data := struct {
	Data []struct{
            MydlinkId string `json:"REMOVE FOR CREDENTIAL"`
	} `json:"data"`
    }{ Data: nil}
    for device := range devList {
        data.Data = append(data.Data, struct{
	    MydlinkId string `json:"REMOVE FOR CREDENTIAL"`
	}{
		MydlinkId: devList[device],
        })
    }

    uap.clearLatestRes()
    api := "REMOVE FOR CREDENTIAL"
    host := uap.HostSite
    if uap.UserToken == "" {
        fmt.Println("Please get UserToken first.")
	return
    }
    urlParameter := req.QueryParam{
        "REMOVE FOR CREDENTIAL": uap.UserToken,
    }
    fmt.Println(data)
    r, err := req.Post("https://" + host + api, req.BodyJSON(&data), urlParameter)
    if err != nil {
        fmt.Println(err)
	return
    }
    var jsonData ResGetDevInfo
    err = r.ToJSON(&jsonData)
    if err != nil {
        fmt.Println(err)
        return
    }
    uap.storeRes(r.Response().StatusCode, int(r.Cost()), jsonData)
}

