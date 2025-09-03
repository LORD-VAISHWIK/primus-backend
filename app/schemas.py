from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    role: str = "client"
    cafe_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    tos_accepted: Optional[bool] = None

class UserOut(UserBase):
    id: int
    role: str
    cafe_id: Optional[int]
    birthdate: Optional[datetime] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    tos_accepted: Optional[bool] = None
    is_email_verified: bool | None = None
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    birthdate: Optional[datetime] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

## Firebase-only: remove legacy OTP schemas

class CafeBase(BaseModel):
    name: str

class CafeCreate(CafeBase):
    owner_id: int

class CafeOut(CafeBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class PCRegister(BaseModel):
    name: str

class PCOut(BaseModel):
    id: int
    name: str
    status: str
    last_seen: datetime
    class Config:
        orm_mode = True

class SessionStart(BaseModel):
    pc_id: int
    user_id: int

class SessionOut(BaseModel):
    id: int
    pc_id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime]
    paid: bool
    amount: float
    class Config:
        orm_mode = True

class WalletTransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    timestamp: datetime
    type: str
    description: str | None

    class Config:
        from_attributes = True

class WalletAction(BaseModel):
    amount: float
    type: str
    description: str | None = None

class GameBase(BaseModel):
    name: str
    exe_path: str
    icon_url: str | None = None
    version: str | None = None
    is_free: bool | None = False
    min_age: int | None = None

class GameOut(GameBase):
    id: int
    last_updated: datetime
    class Config:
        from_attributes = True

class PlatformAccountIn(BaseModel):
    game_id: int
    platform: str
    username: str
    secret: str

class PlatformAccountOut(BaseModel):
    id: int
    game_id: int
    platform: str
    username: str
    in_use: bool
    assigned_pc_id: int | None = None
    assigned_user_id: int | None = None
    class Config:
        from_attributes = True

class LicenseAssignIn(BaseModel):
    game_id: int
    pc_id: int

class LicenseAssignOut(BaseModel):
    id: int
    account_id: int
    user_id: int
    pc_id: int
    game_id: int
    started_at: datetime
    ended_at: datetime | None = None
    class Config:
        from_attributes = True

class PCGameOut(BaseModel):
    id: int
    pc_id: int
    game_id: int
    class Config:
        from_attributes = True

class RemoteCommandIn(BaseModel):
    pc_id: int
    command: str
    params: str | None = None

class RemoteCommandOut(RemoteCommandIn):
    id: int
    issued_at: datetime
    executed: bool

    class Config:
        from_attributes = True

class ChatMessageIn(BaseModel):
    to_user_id: int | None = None
    pc_id: int | None = None
    message: str

class ChatMessageOut(ChatMessageIn):
    id: int
    from_user_id: int
    timestamp: datetime
    read: bool

    class Config:
        from_attributes = True

class NotificationIn(BaseModel):
    user_id: int | None = None
    pc_id: int | None = None
    type: str = "info"
    content: str

class NotificationOut(NotificationIn):
    id: int
    created_at: datetime
    seen: bool

    class Config:
        from_attributes = True

class SupportTicketIn(BaseModel):
    pc_id: int | None = None
    issue: str

class SupportTicketOut(SupportTicketIn):
    id: int
    user_id: int
    status: str
    assigned_staff: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnnouncementIn(BaseModel):
    content: str
    type: str = "info"
    start_time: datetime | None = None
    end_time: datetime | None = None
    target_role: str | None = None

class AnnouncementOut(AnnouncementIn):
    id: int
    created_at: datetime
    active: bool

    class Config:
        from_attributes = True

class HardwareStatIn(BaseModel):
    pc_id: int
    cpu_percent: float
    ram_percent: float
    disk_percent: float
    gpu_percent: float | None = None
    temp: float | None = None

class HardwareStatOut(HardwareStatIn):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class ClientUpdateIn(BaseModel):
    version: str
    description: str | None = None
    file_url: str
    force_update: bool = False

class ClientUpdateOut(ClientUpdateIn):
    id: int
    release_date: datetime
    active: bool

    class Config:
        from_attributes = True

class LicenseKeyIn(BaseModel):
    key: str
    assigned_to: str | None = None
    expires_at: datetime | None = None

class LicenseKeyOut(LicenseKeyIn):
    id: int
    issued_at: datetime
    is_active: bool
    activated_at: datetime | None = None
    last_activated_ip: str | None = None

    class Config:
        from_attributes = True

class LicenseActivateIn(BaseModel):
    key: str
    assigned_to: str

class AuditLogOut(BaseModel):
    id: int
    user_id: int | None = None
    action: str
    detail: str | None = None
    timestamp: datetime
    ip: str | None = None

    class Config:
        from_attributes = True

class PCGroupIn(BaseModel):
    name: str
    description: str | None = None

class PCGroupOut(PCGroupIn):
    id: int
    class Config:
        from_attributes = True

class PCToGroupIn(BaseModel):
    pc_id: int
    group_id: int

class PCToGroupOut(PCToGroupIn):
    id: int
    class Config:
        from_attributes = True

class BackupEntryOut(BaseModel):
    id: int
    backup_type: str
    file_path: str
    created_at: datetime
    note: str | None = None

    class Config:
        from_attributes = True

class PricingRuleIn(BaseModel):
    name: str
    rate_per_hour: float
    group_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    description: str | None = None

class PricingRuleOut(PricingRuleIn):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class WebhookIn(BaseModel):
    url: str
    event: str
    secret: str | None = None

class WebhookOut(WebhookIn):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class MembershipPackageIn(BaseModel):
    name: str
    description: str | None = None
    price: float
    hours_included: float | None = None
    valid_days: int | None = None

class MembershipPackageOut(MembershipPackageIn):
    id: int
    active: bool

    class Config:
        from_attributes = True

class UserMembershipOut(BaseModel):
    id: int
    user_id: int
    package_id: int
    start_date: datetime
    end_date: datetime | None = None
    hours_remaining: float | None = None

    class Config:
        from_attributes = True

class BookingIn(BaseModel):
    pc_id: int
    start_time: datetime
    end_time: datetime

class BookingOut(BookingIn):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class LicenseBase(BaseModel):
    key: str
    cafe_id: int
    expires_at: Optional[datetime]
    max_pcs: int

class LicenseCreate(LicenseBase):
    pass

class LicenseOut(LicenseBase):
    pass

class ClientPCBase(BaseModel):
    name: str
    ip_address: Optional[str]

class ClientPCCreate(ClientPCBase):
    license_key: str

class ClientPCOut(ClientPCBase):
    id: int
    status: str
    last_seen: Optional[datetime]
    cafe_id: int
    license_key: str
    device_id: Optional[str] = None
    bound: bool | None = None
    bound_at: Optional[datetime] = None
    grace_until: Optional[datetime] = None
    suspended: bool | None = None
    class Config:
        from_attributes = True

# Prizes
class PrizeIn(BaseModel):
    name: str
    description: Optional[str] = None
    coin_cost: int
    stock: int

class PrizeOut(PrizeIn):
    id: int
    active: bool
    class Config:
        from_attributes = True

class PrizeRedemptionOut(BaseModel):
    id: int
    user_id: int
    prize_id: int
    timestamp: datetime
    status: str
    class Config:
        from_attributes = True

# Coupons
class CouponIn(BaseModel):
    code: str
    discount_percent: float = 0.0
    max_uses: int | None = None
    per_user_limit: int | None = None
    expires_at: datetime | None = None
    applies_to: str = "*"

class CouponOut(CouponIn):
    id: int
    times_used: int
    class Config:
        from_attributes = True

class CouponRedeemIn(BaseModel):
    code: str
    target: str
    offer_id: int | None = None
    product_id: int | None = None

class CouponRedemptionOut(BaseModel):
    id: int
    coupon_id: int
    user_id: int
    timestamp: datetime
    class Config:
        from_attributes = True

# Leaderboards
class LeaderboardIn(BaseModel):
    name: str
    scope: str = "daily"
    metric: str = "play_minutes"

class LeaderboardOut(LeaderboardIn):
    id: int
    active: bool
    class Config:
        from_attributes = True

class LeaderboardEntryOut(BaseModel):
    id: int
    leaderboard_id: int
    user_id: int
    period_start: datetime
    period_end: datetime
    value: int
    class Config:
        from_attributes = True

# Events
class EventIn(BaseModel):
    name: str
    type: str
    rule_json: str
    start_time: datetime
    end_time: datetime

class EventOut(EventIn):
    id: int
    active: bool
    class Config:
        from_attributes = True

class EventProgressOut(BaseModel):
    id: int
    event_id: int
    user_id: int
    progress: int
    completed: bool
    class Config:
        from_attributes = True

# Offers and Coins
class OfferIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    hours: float

class OfferOut(OfferIn):
    id: int
    active: bool
    class Config:
        from_attributes = True

class UserOfferOut(BaseModel):
    id: int
    user_id: int
    offer_id: int
    purchased_at: datetime
    hours_remaining: float
    class Config:
        from_attributes = True

class CoinTransactionOut(BaseModel):
    id: int
    user_id: int
    amount: int
    timestamp: datetime
    reason: Optional[str] = None
    class Config:
        from_attributes = True

class UserGroupIn(BaseModel):
    name: str
    discount_percent: float = 0.0
    coin_multiplier: float = 1.0
    postpay_allowed: bool = False

class UserGroupOut(UserGroupIn):
    id: int
    class Config:
        from_attributes = True

# Settings
class SettingIn(BaseModel):
    category: str
    key: str
    value: str
    value_type: str = "string"
    description: str | None = None

class SettingUpdate(BaseModel):
    value: str
    value_type: str = "string"
    description: str | None = None

class SettingOut(SettingIn):
    id: int
    updated_by: int | None = None
    updated_at: datetime
    is_public: bool

    class Config:
        from_attributes = True

class SettingsBulkUpdate(BaseModel):
    settings: list[SettingIn]


# Games
class GameBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    enabled: bool = False
    category: str = "game"
    description: Optional[str] = None
    exe_path: Optional[str] = None
    icon_url: Optional[str] = None
    version: Optional[str] = None
    is_free: bool = False
    min_age: Optional[int] = None
    age_rating: int = 0
    tags: Optional[str] = None
    website: Optional[str] = None
    pc_groups: Optional[str] = None
    user_groups: Optional[str] = None
    launchers: Optional[str] = None
    never_use_parent_license: bool = False
    image_600x900: Optional[str] = None
    image_background: Optional[str] = None


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    enabled: Optional[bool] = None
    category: Optional[str] = None
    description: Optional[str] = None
    exe_path: Optional[str] = None
    icon_url: Optional[str] = None
    version: Optional[str] = None
    is_free: Optional[bool] = None
    min_age: Optional[int] = None


class Game(GameBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True
