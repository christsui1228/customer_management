// 店铺枚举
export const ShopBrandEnum = {
    YI: "依",
    LI: "丽",
    MO: "末"
} as const

// 客户来源枚举
export const CustomerSourceEnum = {
    NATURAL_FLOW: "自然流量",
    RECOMMENDED: "推荐"
} as const

// 客户类型枚举
export const CustomerTypeEnum = {
    NEW: "新客户",
    OLD: "老客户",
    CHANGED_NUMBER: "换号"
} as const

// 客户状态枚举
export const CustomerStatusEnum = {
    CONSULTING: "咨询中",
    SAMPLE: "样品",
    PREPARING_ORDER: "准备下单",
    DEAD: "死了"
} as const

// 枚举显示名称映射（与枚举值相同）
export const enumLabels = {
    shop: {
        YI: "依",
        LI: "丽",
        MO: "末"
    },
    source: {
        NATURAL_FLOW: "自然流量",
        RECOMMENDED: "推荐"
    },
    customerType: {
        NEW: "新客户",
        OLD: "老客户",
        CHANGED_NUMBER: "换号"
    },
    customerStatus: {
        CONSULTING: "咨询中",
        SAMPLE: "样品",
        PREPARING_ORDER: "准备下单",
        DEAD: "死了"
    }
}
