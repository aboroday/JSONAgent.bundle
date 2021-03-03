# coding=utf-8

"""
JSONMovieAgent
"""

from utils import Mediafile, open_file, load_json_metadata
from logging import PlexLogAdapter as log
import os
import json

# PLEX API
preferences = Prefs
load_file = Core.storage.load
PlexAgent = Agent.Movies
MediaProxy = Proxy.Media
Metadata = MetadataSearchResult
Trailer = TrailerObject


class JSONAgent(PlexAgent):
    """
    A Plex Metadata Agent for Movies.

    Uses JSON files as the metadata source for Plex Movies.
    """
    name = 'JSONAgent'
    ver = '0.0.1'
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = [
        'com.plexapp.agents.localmedia',
        'com.plexapp.agents.opensubtitles',
        'com.plexapp.agents.podnapisi',
        'com.plexapp.agents.subzero'
    ]
    contributes_to = [
        'com.plexapp.agents.themoviedb',
        'com.plexapp.agents.imdb',
        'com.plexapp.agents.none'
    ]

    # search function
    def search(self, results, media, lang):
        log.debug('# Invoking search function')

        log.info('{plugin} Version: {number}'.format(
            plugin=self.name, number=self.ver))
        log.debug('Plex Server Version: {number}'.format(
            number=Platform.ServerVersion))

        if preferences['debug']:
            log.info('Agent debug logging is enabled!')
        else:
            log.info('Agent debug logging is disabled!')

        mediafile = Mediafile(media.items[0].parts[0].file)
        json_metadata = load_json_metadata(mediafile)

        # Title
        try:
            media.name = json_metadata.get('title')
        except Exception as e:
            log.info('ERROR: No \'title\' tag in JSON. Aborting!')
            log.debug('Exception: {name}'.format(name=e))
            return
        # Sort Title
        try:
            media.title_sort = json_metadata.get('title_sort')
        except:
            log.info('WARNING: No \'title_sort\' tag in JSON.')
            pass
        # ID
        try:
            id = json_metadata.get('id').strip()
        except:
            id = ''
            pass
        if len(id) > 2:
            media.id = id
            log.debug('ID from json: {id}'.format(id=media.id))
        else:
            # if movie id doesn't exist, create
            # one based on hash of title and year
            def ord3(x):
                return '%.3d' % ord(x)

            id = int(''.join(map(ord3, media.name + str(media.year))))
            id = str(abs(hash(int(id))))
            media.id = id
            log.debug('ID generated: {id}'.format(id=media.id))

        results.Append(Metadata(id=media.id, name=media.name, year=media.year, lang=lang, score=100))

        try:
            log.info('Found movie information in JSON file:'
                     ' title = {media.name},'
                     ' id = {media.id}'.format(media=media))
        except:
            pass

    # update function
    def update(self, metadata, media, lang):
        log.debug('# Invoking update function')

        log.info('{plugin} Version: {number}'.format(
            plugin=self.name, number=self.ver))
        log.debug('Plex Server Version: {number}'.format(
            number=Platform.ServerVersion))

        if preferences['debug']:
            log.info('Agent debug logging is enabled!')
        else:
            log.info('Agent debug logging is disabled!')

        mediafile = Mediafile(media.items[0].parts[0].file)
        json_metadata = load_json_metadata(mediafile)

        log.debug('metadata: {name}'.format(name=metadata))

        # Title
        try:
            metadata.title = json_metadata.get('title')
        except Exception as e:
            log.info('ERROR: No \'title\' tag in JSON. Aborting!')
            log.debug('Exception: {name}'.format(name=e))
            return
        # Year
        try:
            metadata.year = int(json_metadata.get('year').strip())
            log.debug('Reading year tag: {year}'.format(year=metadata.year))
        except Exception as e:
            log.debug('WARNING: No \'year\' tag in JSON.')
            log.debug('Exception: {name}'.format(name=e))
            pass

        return metadata
