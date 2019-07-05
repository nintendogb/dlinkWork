package restful

type ResListDevice struct {
    Data []struct {
        HwFeatures []string `json:"REMOVE FOR CREDENTIAL"`
        HwVer string `json:"REMOVE FOR CREDENTIAL"`
    } `json:"data"`
}

type ResGetDevInfo struct {
    Data []struct {
        MydlinkId string `json:"REMOVE FOR CREDENTIAL"`
        Verified bool `json:"REMOVE FOR CREDENTIAL"`
        Features []int `json:"REMOVE FOR CREDENTIAL"`
	PromotionInfo struct {
            Level int `json:"REMOVE FOR CREDENTIAL"`
            Token int `json:"REMOVE FOR CREDENTIAL"`
	} `json:"REMOVE FOR CREDENTIAL"`
    } `json:"data"`
}

type Uap struct {
    HostSite string
    ClientId string
    ClientSecret string
    UserToken string
    Response struct {
       StatusCode int
       JsonData interface {}
       Speed int
    }
}
