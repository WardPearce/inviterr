from typing import List, Optional

from pydantic import BaseModel, Field


class InviteJellyfinPermissions(BaseModel):
    IsAdministrator: Optional[bool] = Field(
        None, description="Indicates if the user is an administrator."
    )
    IsHidden: Optional[bool] = Field(
        None, description="Indicates if the user is hidden."
    )
    EnableCollectionManagement: Optional[bool] = Field(
        None, description="Allows the user to manage collections."
    )
    EnableSubtitleManagement: Optional[bool] = Field(
        None, description="Allows the user to manage subtitles."
    )
    EnableLyricManagement: Optional[bool] = Field(
        None, description="Allows the user to manage lyrics."
    )
    IsDisabled: Optional[bool] = Field(
        None, description="Indicates if the user is disabled."
    )
    MaxParentalRating: Optional[int] = Field(
        None, description="The maximum parental rating allowed for the user."
    )
    BlockedTags: Optional[List[str]] = Field(
        None, description="A list of tags blocked for the user."
    )
    AllowedTags: Optional[List[str]] = Field(
        None, description="A list of tags allowed for the user."
    )
    EnableUserPreferenceAccess: Optional[bool] = Field(
        None, description="Allows the user to access preference settings."
    )
    BlockUnratedItems: Optional[List[str]] = Field(
        None, description="A list of unrated items blocked for the user."
    )
    EnableRemoteControlOfOtherUsers: Optional[bool] = Field(
        None, description="Allows the user to remotely control other users."
    )
    EnableSharedDeviceControl: Optional[bool] = Field(
        None, description="Allows the user to control shared devices."
    )
    EnableRemoteAccess: Optional[bool] = Field(
        None, description="Allows the user to access remotely."
    )
    EnableLiveTvManagement: Optional[bool] = Field(
        None, description="Allows the user to manage live TV settings."
    )
    EnableLiveTvAccess: Optional[bool] = Field(
        None, description="Allows the user to access live TV."
    )
    EnableMediaPlayback: Optional[bool] = Field(
        None, description="Allows the user to play media."
    )
    EnableAudioPlaybackTranscoding: Optional[bool] = Field(
        None, description="Allows audio playback with transcoding."
    )
    EnableVideoPlaybackTranscoding: Optional[bool] = Field(
        None, description="Allows video playback with transcoding."
    )
    EnablePlaybackRemuxing: Optional[bool] = Field(
        None, description="Allows remuxing during playback."
    )
    ForceRemoteSourceTranscoding: Optional[bool] = Field(
        None, description="Forces transcoding for remote sources."
    )
    EnableContentDeletion: Optional[bool] = Field(
        None, description="Allows the user to delete content."
    )
    EnableContentDeletionFromFolders: Optional[List[str]] = Field(
        None, description="A list of folders from which content deletion is allowed."
    )
    EnableContentDownloading: Optional[bool] = Field(
        None, description="Allows the user to download content."
    )
    EnableSyncTranscoding: Optional[bool] = Field(
        None, description="Allows transcoding during sync."
    )
    EnableMediaConversion: Optional[bool] = Field(
        None, description="Allows the user to convert media."
    )
    EnabledDevices: Optional[List[str]] = Field(
        None, description="A list of devices enabled for the user."
    )
    EnableAllDevices: Optional[bool] = Field(
        None, description="Allows the user to access all devices."
    )
    EnabledChannels: Optional[List[str]] = Field(
        None, description="A list of channels enabled for the user."
    )
    EnableAllChannels: Optional[bool] = Field(
        None, description="Allows the user to access all channels."
    )
    InvalidLoginAttemptCount: Optional[int] = Field(
        None, description="The number of invalid login attempts by the user."
    )
    LoginAttemptsBeforeLockout: Optional[int] = Field(
        None, description="The number of login attempts allowed before lockout."
    )
    EnablePublicSharing: Optional[bool] = Field(
        None, description="Allows the user to share content publicly."
    )
    BlockedMediaFolders: Optional[List[str]] = Field(
        None, description="A list of media folders blocked for the user."
    )
    BlockedChannels: Optional[List[str]] = Field(
        None, description="A list of channels blocked for the user."
    )
    RemoteClientBitrateLimit: Optional[int] = Field(
        None, description="The bitrate limit for remote clients."
    )
    SyncPlayAccess: Optional[str] = Field(
        None, description="The user's level of access to SyncPlay."
    )


class InviteEmbyPermissions(BaseModel):
    IsAdministrator: Optional[bool] = Field(
        None, description="Indicates if the user is an administrator."
    )
    IsHidden: Optional[bool] = Field(
        None, description="Indicates if the user is hidden."
    )
    IsHiddenRemotely: Optional[bool] = Field(
        None, description="Indicates if the user is hidden remotely."
    )
    IsDisabled: Optional[bool] = Field(
        None, description="Indicates if the user is disabled."
    )
    MaxParentalRating: Optional[int] = Field(
        None, description="The maximum parental rating allowed."
    )
    BlockedTags: Optional[List[str]] = Field(
        None, description="A list of blocked tags."
    )
    EnableUserPreferenceAccess: Optional[bool] = Field(
        None, description="Indicates if user preference access is enabled."
    )
    BlockUnratedItems: Optional[List[str]] = Field(
        None,
        description="A list of unrated items blocked, such as Movie, Trailer, Series, etc.",
    )
    EnableRemoteControlOfOtherUsers: Optional[bool] = Field(
        None, description="Allows remote control of other users."
    )
    EnableSharedDeviceControl: Optional[bool] = Field(
        None, description="Allows shared device control."
    )
    EnableRemoteAccess: Optional[bool] = Field(
        None, description="Indicates if remote access is enabled."
    )
    EnableLiveTvManagement: Optional[bool] = Field(
        None, description="Allows management of live TV."
    )
    EnableLiveTvAccess: Optional[bool] = Field(
        None, description="Allows access to live TV."
    )
    EnableMediaPlayback: Optional[bool] = Field(
        None, description="Indicates if media playback is enabled."
    )
    EnableAudioPlaybackTranscoding: Optional[bool] = Field(
        None, description="Allows audio playback transcoding."
    )
    EnableVideoPlaybackTranscoding: Optional[bool] = Field(
        None, description="Allows video playback transcoding."
    )
    EnablePlaybackRemuxing: Optional[bool] = Field(
        None, description="Allows playback remuxing."
    )
    EnableContentDeletion: Optional[bool] = Field(
        None, description="Allows content deletion."
    )
    EnableContentDeletionFromFolders: Optional[List[str]] = Field(
        None, description="List of folders from which content deletion is allowed."
    )
    EnableContentDownloading: Optional[bool] = Field(
        None, description="Indicates if content downloading is enabled."
    )
    EnableSubtitleDownloading: Optional[bool] = Field(
        None, description="Allows subtitle downloading."
    )
    EnableSubtitleManagement: Optional[bool] = Field(
        None, description="Allows subtitle management."
    )
    EnableSyncTranscoding: Optional[bool] = Field(
        None, description="Allows sync transcoding."
    )
    EnableMediaConversion: Optional[bool] = Field(
        None, description="Allows media conversion."
    )
    EnabledDevices: Optional[List[str]] = Field(
        None, description="List of enabled devices."
    )
    EnableAllDevices: Optional[bool] = Field(
        None, description="Indicates if all devices are enabled."
    )
    EnabledChannels: Optional[List[str]] = Field(
        None, description="List of enabled channels."
    )
    EnableAllChannels: Optional[bool] = Field(
        None, description="Indicates if all channels are enabled."
    )
    InvalidLoginAttemptCount: Optional[int] = Field(
        None, description="The count of invalid login attempts."
    )
    EnablePublicSharing: Optional[bool] = Field(
        None, description="Allows public sharing."
    )
    BlockedMediaFolders: Optional[List[str]] = Field(
        None, description="List of blocked media folders."
    )
    BlockedChannels: Optional[List[str]] = Field(
        None, description="List of blocked channels."
    )
    RemoteClientBitrateLimit: Optional[int] = Field(
        None, description="Bitrate limit for remote clients."
    )
    ExcludedSubFolders: Optional[List[str]] = Field(
        None, description="List of excluded subfolders."
    )
    DisablePremiumFeatures: Optional[bool] = Field(
        None, description="Indicates if premium features are disabled."
    )
