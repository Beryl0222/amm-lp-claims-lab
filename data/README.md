# 数据说明

所有数据均为合成资料。每张表的首行为字段名。

本演练只核算手续费与回款，不给出市场报价也不发送真实转账。每个分段必须落在同一活跃区间内，上行从进入点计，向下经过边界时采用立即进入的下一区间。失败路由不给任何池记费用或推进价格。所有段的资格按同一全局执行序号，此处撤出只改变有效流动性。协议费按段整数向下取整，再用本段余额分给在区间中的 LP，各自向下取整，分发余数留在池的舍入余项。支付按请求观察顺序，仍有未兑现量可后续另有子付款事实，amount 以最小单位计。金库可用以 lp_deposit 为准，和本金列单独。

## pool_policy

- `pool` 池
- `token0` 币种 A
- `token1` 币种 B
- `protocol_bps` 协议费占费用的基点比例
- `opening_tick` 起始价格档

## initial_positions

- `position` 头寸
- `pool` 池
- `owner` 持有人
- `lower` 下端价格档，包含
- `upper` 上端价格档，不包含
- `liquidity` 流动性单位

## position_ops

- `op` 操作号
- `order` 全局执行顺序
- `known` 观察顺序
- `position` 头寸
- `kind` transfer、remove 或 add
- `holder` 接手人或添加者，可空
- `units` 流动性增加或减少量，可空

## route_legs

- `id` 分段号
- `route` 路由
- `order` 全局执行顺序
- `known` 观察顺序
- `pool` 池
- `from_tick` 进入段时的档
- `to_tick` 离开段时的档
- `asset` 手续费原币
- `fee` 本段总费用
- `revises` 更正引用的段号

## route_receipts

- `receipt` 路由回报号
- `route` 路由号
- `seen` 观察顺序
- `status` fragment、final、failed 或 revision
- `legs` 版本内的完整分段 ID
- `fees` 逐池逐币总费用源快照
- `revises` 若有则为被替代回报

## fee_treasury

- `fact` 托管事实
- `step` 观察顺序
- `pool` 池
- `asset` 币
- `kind` lp_deposit、principal、claim、submitted、paid 或 failed
- `owner` 请求人，可空
- `payment` 提现标识，池币内唯一
- `amount` 最小单位
